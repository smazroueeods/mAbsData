# Monoclonal Antibodies 


### Monoclonal Antibodies Data Table


| Index  | Field                |
| :----- | :------------------- |
| 0      | mab_uid              |
| 1      | mab_name             |
| 2      | cross_reference      |
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
│ mAb │
└─┬─┬─┘
  │ │
  │ │
  │ │
  │ │ targets                ┌───────┐
  │ └───────────────────────►│ virus │
  │                          └───────┘
  │                              ▲
  │                              │
  │ treats   ┌─────────┐  causes │
  └─────────►│ disease ├─────────┘
             └─────────┘
```
 

### Document Structure


###### Antibody-Virus Relationship
```JSON

{
    "subject": {
        "id": "",
        "cross_reference": {}
    },
    "relation": {
        "epitope": {},
        "pubmed": ""
    },
    "object": {
        "id": "",
        "name": "",
        "family": "",
        "species": ""
    }
}
```

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
