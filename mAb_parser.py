
import csv
import os

# Convert csv into a list of dicts
def read_csv(file: str, delim: str):
    info = []
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=delim)
        categories: list[str]
        i = 0
        for row in reader:
            if len(row) == 0:
                continue
            if i == 0:
                categories = row
            else:
                info.append({})
                for j in range(len(row)):
                    info[i-1][categories[j]] = row[j]
            i += 1
    return info

def load_data(data_folder: str):
    # Read files for mAbs KG
    mab_info = read_csv(os.path.join(data_folder, "NCATS_MonoClonalAntibodies.csv"), ",")

    docs: dict[str, any] = {}

    # Create JSON for mAbs/virus/disease
    for row in mab_info:
        doc_id = f"{row['MAB_ID']}-{row['VIRUS_ID']}"

        # Just append virus if we have already processed mAb-virus pair
        if doc_id in docs:
            docs[doc_id]['relation'].append({
                'VIRUS_ID': int(row['VIRUS_ID']),
                'VIRUS_NAME': row['VIRUS_NAME'],
            })
        else:
            docs[doc_id] = {
                '_id': doc_id,
                'subject': {
                    "type": "Antibody",
                    "name": row['MAB_NAME'],
                    'id': row['MAB_ID'],
                },
                'object': {
                    "type": "Virus",
                    'id': int(row['VIRUS_ID']),
                    'name': row['VIRUS_NAME'],
                },
                # 'relation': [{
                #     'VIRUS_ID': int(row['VIRUS_ID']),
                #     'VIRUS_NAME': row['VIRUS_NAME'],
                # }],
                "pubmed": <pubmed_id>,
                'predicate': 'targets'
            }

    for row in virus_disease_info:
        doc_id = f"{row['VIRUS_ID']}-{row['DISEASE_ID']}"

        # Just append disease if we have already processed virus-disease pair
        if doc_id in docs:
            docs[doc_id]['relation'].append({
                'DISEASE_ID': int(row['DISEASE_ID']),
                'DISEASE_NAME': row['DISEASE_NAME'],
            })
        else:
            docs[doc_id] = {
                '_id': doc_id,
                'subject': {
                    'VIRUS_NAME': row['VIRUS_NAME'],
                    'VIRUS_ID': int(row['VIRUS_ID']),
                },
                'object': {
                    'DISEASE_ID': row['DISEASE_ID'],
                    'DISEASE_NAME': row['DISEASE_NAME'],
                },
                'relation': [{
                    'DISEASE_ID': row['DISEASE_ID'],
                    'DISEASE_NAME': row['DISEASE_NAME'],
                }],
                'predicate': 'causes'
            }

# '_id': doc_id,
#                 'subject': {
#                     "type": "ChemicalMiture",
#                     'id': row['mab_id'],
#                     "name": row['mab_name'],
#                 },
#                 'object': {
#                     "type": "Virus",
#                     'id': int(row['virus_id']),
#                     'name': row['virus_name'],
#                 },
#                 "pubmed": <pubmed_id>,
#                 'predicate': 'targets'
#             }



# '_id': doc_id,
#                 'subject': {
#                     "type": "virus",
#                     "name": row['virus_name'],
#                     'id': row['virus_id'],
#                 },
#                 'object': {
#                     "type": "disease",
#                     "id": int(row['disease_id']),
#                     'name': row['disease_name'],
#                 },
#                 'predicate': 'causes'
#             }




# '_id': doc_id,
#                 'subject': {
#                     "type": "disease",
#                     "id": row['disease_id'],
#                     "name": row['disease_name'],
#                 },
#                 'object': {
#                     "type": "phenotypic_feature",
#                     'id': int(row['phetotypic_feature_id']),
#                     'name': row['phenotypic_feature_name'],
#                 },
#                 'predicate': 'exhibits'
#             }





# '_id': doc_id,
#                 'subject': {
#                     "type": "Antibody",
#                     "id": row['mab_id'],
#                     "name": row['mab_name'],
#                 },
#                 'object': {
#                     "type": "phenotypic_feature",
#                     "id": int(row['symptom_id']),
#                     "name": row['symptom_name'],
#                 },
#                 'predicate': 'ameliorates'
#             }




# '_id': doc_id,
#                 'subject': {
#                     "type": "ChemicalMixture",
#                     'id': row['mab_id'],
#                     "name": row['mab_name'],
#                 },
#                 'object': {
#                     "type": "disease",
#                     'id': int(row['disease_id']),
#                     'name': row['disease_name'],
#                 },
#                 'predicate': 'treats'
#             }




# '_id': doc_id,
#                 'subject': {
#                     "type": "ChemicalMixture",
#                     'id': row['mab_id'],
#                     "name": row['mab_name'],
#                 },
#                 'object': {
#                     "type": "gene",
#                     'id': int(row['gene_id']),
#                     'name': row['gene_name'],
#                 },
#                 'predicate': 'interacts with'
#             }



    
    for doc_id in docs:
        yield docs[doc_id]

def test():
    import json

    obj = {'data': []}
    for i in load_data("./data"):
        obj['data'].append(i)

    with open("./output_mabs.json", "w") as f:
        f.write(json.dumps(obj, indent=2))

if __name__ == '__main__':
    test()
