import couchdb
import uuid
import random
import requests
uuid.uuid4()


def delete_all_documents(db):
    for doc_id in db:
        doc = db[doc_id]
        db.delete(doc)

def print_document(doc):
    print(f"Document ID: {doc['_id']}")
    for key, value in doc.items():
        print(f"{key}: {value}")

couch = couchdb.Server('http://admin:password@localhost:5984/')

def bulk_get_data(db_url, docs_payload):
    endpoint = f"{db_url}/_bulk_get"

    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(endpoint, json=docs_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
# Specify the database name
db = 'my_database'

# Check if the database already exists
if db in couch:
    print("Database already exists.")
else:
    # Create a new database
    db = couch.create(db)
    print("Database created:", db)

db = couch['my_database']

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

# Create documents
for doc in documents:
    db.save(doc)

# Test if documents were inserted
print("Inserted documents:")
for doc_id in db:
    doc = db[doc_id]
    print(f"Name: {doc['name']}, Age: {doc['age']}, Address: {doc['address']}, Occupation: {doc['occupation']}")

# Prints our our documents with all its parameters
for doc_id in db:
    doc = db[doc_id]
    print_document(doc)

design_doc = {
    "_id": "_design/mydesign",
    "views": {
        "names_and_ages": {
            "map": "function(doc) { if (doc.name && doc.age) { emit(doc.name, doc.age); } }"
        }
    }
}

db.save(design_doc)

print("\nView results (Names and Ages):")
for row in db.view('mydesign/names_and_ages'):
    print(f"Name: {row.key}, Age: {row.value}")

# db_url = 'http://admin:password@localhost:5984/'
# document_ids = ["doc1", "doc2", "doc4"]
# result = bulk_get_data(db_url, db, document_ids)
# if result:
#     print(result)
# else:
#     print("Failed to retrieve data.")


db_url = "http://admin:password@localhost:5984/my_database"  # Replace with the URL of your CouchDB server and the database name
docs_payload = {
    "docs": [
        {
            "id": "doc1",
            
        },
        {
            "id": "doc3",
            
        },
        {
            "id": "doc5"
        }
    ]
}

result = bulk_get_data(db_url, docs_payload)
if result:
    print(result)
else:
    print("Failed to fetch data.")

# import requests

# def bulk_get_data(db_url, db_name, doc_ids):
#     endpoint = f"{db_url}/{db_name}/_all_docs"

#     # Prepare the payload for the POST request
#     bulk_get_request = {
#         "keys": doc_ids
#     }

#     try:
#         response = requests.post(endpoint, json=bulk_get_request)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return None

# # Example usage:
# db_url = "http://admin:password@localhost:5984/"  # Replace with the URL of your CouchDB server
# db_name = "my_database"  # Replace with your actual database name
# document_ids = ["doc1", "doc3", "doc5"]  # Replace with the desired document IDs

# result = bulk_get_data(db_url, db_name, document_ids)
# if result:
#     print(result)
# else:
#     print("Failed to fetch data.")

#jedním dotazem získat vektor dokumentů pomocí ID

