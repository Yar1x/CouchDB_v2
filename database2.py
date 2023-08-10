import couchdb
import torch
from torch.utils.data import Dataset

# Loading data using PyTorch library

def fetch_data_from_couchdb(db_url, db_name, doc_ids):
    server = couchdb.Server(db_url)
    db = server[db_name]

    data = []
    for doc_id in doc_ids:
        try:
            doc = db.get(doc_id)
            if doc is not None:
                data.append(doc)
        except couchdb.http.ResourceNotFound:
            print(f"Document with ID '{doc_id}' not found in the database.")
    
    return data

class CouchDBDataSet(Dataset):
    def __init__(self, db_url, db_name, doc_ids):
        self.data = fetch_data_from_couchdb(db_url, db_name, doc_ids)
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

from torch.utils.data import DataLoader

def create_data_loader(db_url, db_name, doc_ids, batch_size=1, shuffle=True):
    dataset = CouchDBDataSet(db_url, db_name, doc_ids)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return data_loader


db_url = "http://admin:password@localhost:5984/"
db_name = "students"
doc_ids = ["student_id_1", "teacher_id_2", "class_id_1"]  # Replace with the document IDs you want to fetch

data_loader = create_data_loader(db_url, db_name, doc_ids, batch_size=1, shuffle=False)

for batch in data_loader:
    # Your training or evaluation code here
    print(batch)  # Batch will contain the data from CouchDB
