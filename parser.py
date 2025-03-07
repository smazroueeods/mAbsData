from typing import Any, Generator
import collections
import csv
import itertools
import json
import logging
import pathlib
import re
import urllib
import urllib.request


logger = logging.getLogger("mabs")
logger.setLevel("DEBUG")


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


def _filter_document(entry: Any, *forbidden: list) -> Any:
    """
    Filters the document for any forbidden entries provided.

    Used within the plugin to remove falsy values like None or ''
    """
    if isinstance(entry, list):
        return [
            _filter_document(inner_entry, *forbidden)
            for inner_entry in entry
            if inner_entry not in forbidden
        ]
    elif isinstance(entry, dict):
        result = {}
        for key, value in entry.items():
            value = _filter_document(value, *forbidden)
            if key not in forbidden and value not in forbidden:
                result[key] = value
        return result
    return entry


def _parse_cross_reference(raw_cross_reference_value: str) -> collections.defaultdict:
    """
    Parser for the cross reference values

    Example entries for structure:
    [0] PDB: 2R69
    [1] PDB: 6WEQ, PDB: 7K93
    [2] PDB: 2I69 and 1SVB
    [3] PDB: 5JHM, 5JHL

    Split on [",", "and"]
    [0] ["PDB: 2R69"]
    [1] ["PDB: 6WEQ", "PDB: 7K93"]
    [2] ["PDB: 2I69", "1SVB"]
    [3] ["PDB: 5JHM", "5JHL"]
    """
    cross_reference = collections.defaultdict(list)
    if raw_cross_reference_value is not None and raw_cross_reference_value != "":
        creference = raw_cross_reference_value.strip()
        creference_chunks = re.split(r",|and", creference)

        prior_chunk_header = None
        for chunk in creference_chunks:
            cr_split_chunk = chunk.split(":")

            if len(cr_split_chunk) == 1:
                cr_value = cr_split_chunk[0].strip()
                cross_reference[prior_chunk_header].append(cr_value)

            elif len(cr_split_chunk) == 2:
                cr_header = cr_split_chunk[0].strip()
                cr_value = cr_split_chunk[1].strip()
                cross_reference[cr_header].append(cr_value)
                prior_chunk_header = cr_header
    return cross_reference


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


def _create_antibody_virus_document(row: dict) -> dict:
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
    cross_reference = _parse_cross_reference(row.get("Protein_RefID", None))

    epitope = {"protein": None, "domain": None, "description": None}
    if row.get("Epitope", None) is not None:
        epitope_contents = row["Epitope"].split(",")

        if len(epitope_contents) > 3:
            description_overflow = []
            while len(epitope_contents) > 2:
                description_overflow.append(epitope_contents.pop(-1))
            description_overflow.reverse()
            epitope_contents.append("".join(description_overflow))

        for epitope_value, key_value in itertools.zip_longest(
            epitope_contents, epitope.keys(), fillvalue=None
        ):
            if epitope_value is not None:
                epitope[key_value] = epitope_value

    pubmed_collection = []
    if row["pubmed_id"] is not None:
        pubmed_collection = [
            pubmed_id.strip() for pubmed_id in row["pubmed_id"].split(",")
        ]

    document = {
        "_id": f"{row['mab_name']}-{row['virus_id']}",
        "subject": {"id": row["mab_name"], "cross_reference": cross_reference},
        "relation": {"epitope": epitope, "pubmed": pubmed_collection},
        "object": {
            "id": row["virus_id"],
            "name": row["virus_name"],
            "type": "Virus",
            "family": row["Family"],
            "species": row["Species"],
        },
    }

    document = _filter_document(document, *["", None, {}])
    return document


def _create_antibody_protein_document(row: dict) -> Generator[dict, str, None]:
    """
    Generates the document detailing the subject-relation-object
    structure between the antibody and protein
    """
    cross_reference = _parse_cross_reference(row.get("Protein_RefID", None))

    target_protein = []
    if row.get("Target Protein") is not None:
        target_protein = row["Target Protein"].split(",")

    targets = []
    if row.get("Target") is not None:
        targets = row["Target"].split(",")

    pubmed_collection = []
    if row["pubmed_id"] is not None:
        pubmed_collection = [
            pubmed_id.strip() for pubmed_id in row["pubmed_id"].split(",")
        ]

    for target in targets:
        if "UniProt" in target:
            protein_target = target.split(":")
            protein_object_id = f"UniProtKB:{protein_target[1].split()[0]}"

            document = {
                "_id": f"{row['mab_name']}-{target}",
                "subject": {"id": row["mab_name"], "cross_reference": cross_reference},
                "relation": {"pubmed": pubmed_collection},
                "object": {"id": protein_object_id, "type": "Protein"},
            }
            document = _filter_document(document, *["", None, {}])
            yield document


def load_data(data_folder: str):
    """
    Load data and process JSON structure
    """
    # Create JSON for mAbs/virus/disease
    data_folder = pathlib.Path(data_folder).resolve().absolute()
    antibodies_file = data_folder.joinpath("NCATS_MonoClonalAntibodies.csv")
    for row in _read_csv(str(antibodies_file), delim=","):
        antibody_virus_document = _create_antibody_virus_document(row)
        yield antibody_virus_document

        yield from _create_antibody_protein_document(row)
