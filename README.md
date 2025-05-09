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


### Relationship Diagram

`antibody -> protein -> virus`


### Document Structure


###### Antibody-Protein Relationship

```JSON
{
    "subject": {
        "id": "",
        "cross_reference": {}
        "type": "",
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

###### Virus-Disease Relationship

```JSON
{
    "_id": "", 
    "subject": {
        "id": "", 
        "name": "", 
        "family": "", 
        "species": [], 
        "type": ""
    }, 
    "relation": {
        "pubmed": []
    }, 
    "object": {
        "id": "", 
        "type": ""
    }
}
```

###### Antibody-Virus Relationship

```JSON
{
    "_id": "",
    "subject": {
        "id": "",
        "cross_reference": {}
        "type": "",
    },
    "relation": {
        "pubmed": []
    },
    "object": {
        "id": "",
        "name": "",
        "type": ""
        "family": "",
        "species": "",
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
    },
    { // virus-disease
        "_id": "11053-DOID:12205", 
        "subject": {
            "id": "11053", 
            "name": "DENV1", 
            "family": "Flavivirus", 
            "species": ["DENV", "WNV", "ZIKV"], 
            "type": "Virus"
        }, 
        "relation": {
            "pubmed": [
                "18264114",
                "9657950", 
                "24743696", 
                "22723463", 
                "22235356", 
                "21264311", 
                "20369024",
                "18562544", 
                "27475895", 
                "35432292", 
                "16809304", 
                "32015557", 
                "27882950", 
                "25501631",
                "25581790",
                "33317184", 
                "27974667",
                "27417494", 
                "10361725", 
                "22285214", 
                "22491255",
                "23851440", 
                "27707930",
                "31945137",
                "24255124",
                "24421336",
                "26355030", 
                "33414220"
            ]
        }, 
        "object": {
            "id": "DOID:12205", 
            "type": "Disease"
        }
    },
    { // antibody-virus
        "_id": "DENV1-E113-11053", 
        "subject": {
            "id": "DENV1-E113", 
            "type": "Antibody"
        }, 
        "relation": {
            "pubmed": ["20369024"]
        }, 
        "object": {
            "id": "11053", 
            "name": "DENV1", 
            "type": "Virus", 
            "family": "Flavivirus", 
            "species": "DENV"
        }
    }
]
```
