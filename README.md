# Monoclonal Antibodies 


### Monoclonal Antibodies Data Table


| Index  | Field                |
| :----- | :------------------- |
| 0      | mab_uid              |
| 1      | mab_name             |
| 2      | Protein_RefID        |
| 3      | virus_id             |
| 4      | virus_name           |
| 5      | Family               |
| 6      | Organism             |
| 7      | Species              |
| 8      | Epitope              |
| 9      | pubmed_id            |
| 10     | Target Protein       |
| 11     | Target type          |
| 12     | Target               |
| 13     | Target name          |
| 14     | Assay type           |
| 15     | Assay                |
| 16     | Quantitative measure |
| 17     | Unit                 |
| 18     | disease_id           |
| 19     | disease_name         |


### Relationship Diagram

`antibody -> protein -> virus`


### Document Structure


###### Antibody-Protein Relationship

```JSON
{
    "subject": {
        "id": "",
        "type": "",
        "cross_reference": {}
    },
    "relation": {
        "pubmed": []
    },
    "object": {
        "id": "",
        "name": "",
        "type": ""
    }
}
```


###### Protein-Virus Relationship

```JSON
{
    "_id": "",
    "subject": {
        "id": "",
        "type": "",
    },
    "relation": {
        "pubmed": []
    },
    "object": {
        "id": "",
        "name": "",
        "family": "",
        "species": "",
        "type": ""
    }
}
```



### Document Examples

```JSON
[
    { // antibody-protein
        "_id": "FabZK2B10-UniProtKB:A0A024B7W1",
        "subject": {
            "id": "FabZK2B10",
            "cross_reference": {
                "PDB": [
                    "6JEP"
                ]
            },
            "type": "Antibody"
        },
        "relation": {
            "pubmed": [
                "29719255",
                "30893607"
            ]
        },
        "object": {
            "id": "UniProtKB:A0A024B7W1",
            "type": "Protein"
        }
    },
    { // protein-virus
        "_id": "UniProtKB:Q6RVA2-11069",
        "subject": {
            "id": "UniProtKB:Q6RVA2",
            "type": "Protein"
        },
        "relation": {
            "pubmed": [
                "27158114",
                "21264311"
            ]
        },
        "object": {
            "id": "11069",
            "name": "DENV3",
            "family": "Flavivirus",
            "species": "DENV",
            "type": "Virus"
        }
    }
]
```
