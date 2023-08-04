import torch
from torch.utils.data import Dataset, DataLoader
import couchdb

# Custom DataSet for CouchDB
class CouchDBDataset(Dataset):
    def __init__(self, db, document_ids):
        self.db = db
        self.document_ids = document_ids

    def __len__(self):
        return len(self.document_ids)

    def __getitem__(self, idx):
        doc_id = self.document_ids[idx]
        document = self.db[doc_id]
        # Implement logic to preprocess and extract features/labels from the document
        # Example: return document['features'], document['label']
        return {
            'name': document['name'],
            'age': document['age'],
            'occupation': document['occupation']
        }

# CouchDB connection and database
server = couchdb.Server('http://admin:password@localhost:5984/')
db_name = 'my_database'
db = server[db_name]

def delete_all_documents(db):
    for doc_id in db:
        doc = db[doc_id]
        db.delete(doc)

if db_name in server:
    print("Database already exists.")
else:
    # Create a new database
    db = server.create(db)
    print("Database created:", db)

documents = [
    {
        "_id": "doc1",
        "name": "Alice",
        "age": 30,
        "address": {
            "street": "769 Villa Drive",
            "city": "South Bend",
            "state": "IN",
            "zip": "46618"
        },
        "occupation": "Engineer"
    },
    {
        "_id": "doc2",
        "name": "Bob",
        "age": 25,
        "address": {
            "street": "1151 Kyle Street",
            "city": "Grand Island",
            "state": "NE",
            "zip": "68801"
        },
        "occupation": "Engineer"
    },
    {
        "_id": "doc3",
        "name": "Charlie",
        "age": 35,
        "address": {
            "street": "2453 Heather Sees Way",
            "city": "Welch",
            "state": "OK",
            "zip": "74369"
        },
        "occupation": "Developer"
    },
    {
        "_id": "doc4",
        "name": "David",
        "age": 28,
        "address": {
            "street": "2843 Bassell Avenue",
            "city": "Wichita",
            "state": "AR",
            "zip": "67202"
        },
        "occupation": "Manager"
    },
    {
        "_id": "doc5",
        "name": "Eve",
        "age": 22,
        "address": {
            "street": "1578 Catherine Drive",
            "city": "Jamestown",
            "state": "ND",
            "zip": "58401"
        },
        "occupation": "Intern"
    }
]

delete_all_documents(db)
for doc in documents:
    db.save(doc)

# List of document IDs you want to fetch
document_ids = ['doc1', 'doc3', 'doc4']

# Create custom dataset with CouchDB database and document IDs
dataset = CouchDBDataset(db, document_ids)

# Create DataLoader with batch size and other options
batch_size = 1
shuffle = False
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

# Iterate over the data_loader during training
for batch_data in data_loader:
    for name, age, occupation in zip(batch_data['name'], batch_data['age'], batch_data['occupation']):
    # Your training logic using batch_data
        print(f"Name: {name} aged {age} is {occupation}")
    

