import csv
import itertools
import json
import logging
import pathlib
from typing import Generator
import urllib
import urllib.request
import uuid


logger = logging.getLogger("mabs")
logger.setLevel("DEBUG")


disease_lookup_table = {}


def _normalize_row(row: dict) -> bool:
    """
    Normalize the rows to ensure that the expected
    values exist in order to generate a document
    """
    valid_row = True
    if not row.get("mab_uid") or not row.get("virus_id") or not row.get("virus_name"):
        logger.debug(
            "Missing required fields {'mab_uid', 'virus_id', 'virus_name'} in row:%s\n",
            json.dumps(row, indent=2),
        )
        valid_row = False

    try:
        int(row["virus_id"])
    except ValueError:
        logger.debug("Invalid virus_id value in row: %s", row)
        valid_row = False

    for key, value in row.items():
        if value is not None and isinstance(value, str):
            row[key] = value.strip()

    return valid_row


def _read_csv(file: str, delim: str) -> Generator[dict, str, None]:
    """
    Generator for the csv data file to produce
    a collection of dictionaries from the rows
    """
    with open(file, encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=None, delimiter=delim)
        for index, row in enumerate(reader):
            if len(row) == 0:  # Skip empty rows
                logger.debug("Row index %s. Skipping empty row", index)
            elif len(row) != len(reader.fieldnames):  # Row length mismatch
                logger.debug(
                    "Row index %s. Skipping due to row length mismatch: %s", index, row
                )
            else:  # yield row
                if _normalize_row(row):
                    yield row


def _create_anitbody_virus_document(row: dict) -> dict:
    """
    Generates the document detailing the subject-relation-object
    structure between the antibody and virus

    cross_reference example values:
        > Cellosaurus: CVCL_J890
        > PDB: 2R69
        > Addgene: 120363
        > PDB: 2I69 and 1SVB

    epitope example values:
        > Envelope protein E
        > Envelope protein E, Fusion loop domain (98-DRXW-101)
        > Envelope protein E, EDIII domain, This antibody neutralizes dengue virus serotypes 1, 2 and 3.
    """

    cross_reference = {}
    if row.get("cross_reference", None) is not None:
        cr_name, cr_value = row["cross_reference"]
        cr_name = cr_name.strip('"')
        cr_value = cr_value.split("and")

    epitope = {"protein": None, "domain": None, "description": None}
    if row.get("epitope", None) is not None:
        epitope_contents = row["epitope"].split(",")
        for epitope_value, key_value in itertools.zip_longest(
            epitope_contents, epitope.keys(), fillvalue=None
        ):
            epitope[key_value] = epitope_value

    virus_id = (int(row["virus_id"]),)
    document = {
        "_id": f"{uuid.uuid4()}-{row['mab_name']}-{virus_id}",
        "subject": {"id": row["mab_name"], "cross_reference": cross_reference},
        "relation": {"epitope": epitope, "pubmed": row["pubmed_id"]},
        "object": {
            "id": int(row["virus_id"]),
            "name": row["virus_name"],
            "family": row["Family"],
            "species": row["Species"],
        },
        "predicate": "targets",
    }
    return document


def _create_anitbody_protein_document(row: dict) -> Generator[dict, str, None]:
    """
    Generates the document detailing the subject-relation-object
    structure between the antibody and protein
    """
    cross_reference = {}
    if row.get("cross_reference") is not None:
        cr_name, cr_value = row["cross_reference"]
        cr_name = cr_name.strip('"')
        cr_value = cr_value.split("and")

    target_protein = []
    if row.get("Target Protein") is not None:
        target_protein = row["Target Protein"].split(",")

    targets = []
    if row.get("Target") is not None:
        targets = row["Target"].split(",")

    for target in targets:
        document = {
            "_id": f"{uuid.uuid4()}-{row['mab_name']}-{target}",
            "subject": {"id": row["mab_name"], "cross_reference": cross_reference},
            "relation": {"pubmed": row["pubmed_id"]},
            "object": {"id": target, "name": target_protein},
            "predicate": "placeholder",
        }
        yield document


def _create_anitbody_disease_document(row: dict) -> dict:
    """
    Generates the document detailing the subject-relation-object
    structure between the antibody and disease
    """
    cross_reference = {}
    if row.get("cross_reference") is not None:
        cr_name, cr_value = row["cross_reference"]
        cr_name = cr_name.strip('"')
        cr_value = cr_value.split("and")

    disease_name = row["disease_name"]
    discovered_disease_name = _disease_name_lookup(disease_name)

    document = {
        "_id": f"{uuid.uuid4()}-{row['mab_name']}-{row['disease_id']}",
        "subject": {"id": row["mab_name"], "cross_reference": cross_reference},
        "relation": {"pubmed": row["pubmed_id"]},
        "object": {"id": row["disease_id"], "name": discovered_disease_name},
        "predicate": "treats",
    }
    return document


def _disease_name_lookup(disease_name: str) -> str:
    """
    Perform a lookup on my disease for a corresponding disease name.

    Regardless of result, we update the result to a lookup table as
    in-memory cache to avoid unnecessary network calls
    """
    discovered_disease_name = disease_lookup_table.get(disease_name, None)
    if discovered_disease_name is None:
        try:
            disease_url_lookup = f"https://mydisease.info/v1/disease/{disease_name}?fields=disgenet.xrefs.disease_name"
            with urllib.request.urlopen(disease_url_lookup) as http_response:
                response_content = http_response.read()
                response_body = json.loads(response_content.decode("utf-8"))
                discovered_disease_name = response_body["disgenet"]["xrefs"][
                    "disease_name"
                ]
        except urllib.error.HTTPError:
            discovered_disease_name = None
        finally:
            disease_lookup_table[disease_name] = discovered_disease_name
    return discovered_disease_name


def load_data(data_folder: str):
    """
    Load data and process JSON structure
    """
    # Create JSON for mAbs/virus/disease
    data_folder = pathlib.Path(data_folder).resolve().absolute()
    antibodies_file = data_folder.joinpath("NCATS_MonoClonalAntibodies.csv")
    for row in _read_csv(str(antibodies_file), delim=","):
        antibody_virus_document = _create_anitbody_virus_document(row)
        yield antibody_virus_document

        antibody_disease_document = _create_anitbody_disease_document(row)
        yield antibody_disease_document

        yield from _create_anitbody_protein_document(row)
