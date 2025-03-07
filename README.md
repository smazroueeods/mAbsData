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

```
┌─────┐
│     │
│ mAb │
│     │
└┬─┬─┬┘           ┌─────────┐
 │ │ │            │         │
 │ │ └───────────►│  virus  │
 │ │              │         │
 │ │              └─────────┘
 │ │              ┌─────────┐
 │ │              │         │
 │ └─────────────►│ protein │
 │                │         │
 │                └─────────┘
 │                ┌─────────┐
 │                │         │
 └───────────────►│ disease │
                  │         │
                  └─────────┘
```
 

### Document Structure


###### Antibody-Protein Relationship

```JSON
{
    "subject": {
        "id": "",
        "cross_reference": {}
    },
    "relation": {
        "pubmed": ""
    },
    "object": {
        "id": "",
        "name": ""
    }
}
```


### Document Examples

```JSON
[
    { // antibody-protein
        "subject": {
            "id": "1A1D-2",  // from column mab_name
            "cross_reference": {    // from column Protein_RefID
                "PDB": ["2R69"]
            }
        },
        "relation": {
            "pubmed": ["18264114", "9657950"]  // from column pubmed_id
        },
        "object": {
            "uniprot": "P29991"  // from column Target
        }
    }
]
```
