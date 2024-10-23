import json

# Sample data
data_mabVirus = {
    "subject": {
        "type": "Treatment",
        "id": <mAb_UID>,
        "xrefs": {
            "CrossReference": "PDB: 2R69",
            "Publications": ["PMID: 26265529"]
        }
    },
    "object": {
        "type": "Virus",
        "id": <Virus_ID>,
        "xrefs": {
            "ncbi": "11060",
        }
    },
    "predicate": "targets",

}


# Convert to JSON string for representation
json_data1 = json.dumps(data_mabVirus, indent=4)
print(json_data1)

# Sample data
data_VirusDisease = {
    "subject": {
        "type": "Virus",
        "id": <zVirus_ID>,
        "xrefs": {
            "CrossReference": "11060",
            "Publications": ["PMID: 18264114"]
        }
    },
    "object": {
        "type": "Disease",
        "id": <Disease_ID>,
        "xrefs": {
            "ncbi": "12205",
        }
    },
    "predicate": "causes",

}

# Convert to JSON string for representation
json_data2 = json.dumps(data_VirusDisease, indent=4)
print(json_data2)