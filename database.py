import asyncio
import couchdb
import requests

# Loading data with ids using HTTP Request _bulk_get

# Server setup

server = couchdb.Server('http://admin:password@localhost:5984/')

# Name of the database
db_name = 'students'

# Check if DB exists with the given name
if db_name in server:
    print("Database already exists.")
else:
    # Create a new database
    db = server.create(db_name)
    print("Database created:", db)

db = server[db_name]


# Creating a function that represents _bulk_get http request
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

# Creating a structure of documents
student_documents = [
    {
        "_id": "student_id_1",
        "name": "Alice",
        "surname": "McKenzie",
        "age": 20,
        "address": {
            "street": "769 Villa Drive",
            "city": "South Bend",
            "state": "IN",
            "zip": "46618"
        },
    },
    {
        "_id": "student_id_2",
        "name": "Bob",
        "surname": "Cody",
        "age": 25,
        "address": {
            "street": "1151 Kyle Street",
            "city": "Grand Island",
            "state": "NE",
            "zip": "68801"
        },
    },
    {
        "_id": "student_id_3",
        "name": "Charlie",
        "surnme": "Shein",
        "age": 18,
        "address": {
            "street": "2453 Heather Sees Way",
            "city": "Welch",
            "state": "OK",
            "zip": "74369"
        },
    },
    {
        "_id": "student_id_4",
        "name": "David",
        "surname": "Bronwick",
        "age": 22,
        "address": {
            "street": "2843 Bassell Avenue",
            "city": "Wichita",
            "state": "AR",
            "zip": "67202"
        },
    },
    {
        "_id": "student_id_5",
        "name": "Eve",
        "surname": "Byrne",
        "age": 20,
        "address": {
            "street": "1578 Catherine Drive",
            "city": "Jamestown",
            "state": "ND",
            "zip": "58401"
        },
    }
]

teacher_documents = [
    {
        "_id": "teacher_id_1",
        "name": "John",
        "surname": "Doe",
        "age": 35,
        "address": {
            "street": "123 Main Street",
            "city": "Anytown",
            "state": "Somestate",
            "zipcode": "12345"
            }
    },
    {
        "_id": "teacher_id_2",
        "name": "Jane",
        "surname": "Smith",
        "age": 42,
        "address": {
            "street": "456 Elm Street",
            "city": "Othertown",
            "state": "Otherstate",
            "zipcode": "54321"
            }
    },
    {
        "_id": "teacher_id_3",
        "name": "Robert",
        "surname": "Johnson",
        "age": 28,
        "address": {
            "street": "789 Oak Avenue",
            "city": "Anycity",
            "state": "Anotherstate",
            "zipcode": "98765"
            }
    }

]

class_documents = [
    {
        "_id": "class_id_1",
        "name": "EL",
        "teacher": "teacher_id_1",
        "students": ["student_1", "student_3"]
    },
    {
        "_id": "class_id_2",
        "name": "KB",
        "teacher": "teacher_id_3",
        "students": ["student_5"]
    },
    {
        "_id": "class_id_3",
        "name": "STR",
        "teacher": "teacher_id_2",
        "students": ["student_2", "student_4"]
    }
]

all_documents = student_documents + teacher_documents + class_documents


# Creating documents
# for docs in all_documents:
#     db.save(docs)

# Test if documents were inserted
# print("Inserted documents:")
# for doc_id in db:
#     doc = db[doc_id]
#     print(f"''Doc id: {doc['_id']} ; Name: {doc['name']}")

db_url = "http://admin:password@localhost:5984/students"

# Structure for finding documents by ID
document_ids = {
    "docs": [

    
    {"id": "student_id_1"},
    {"id": "student_id_5"},
    {"id": "teacher_id_3"},
    {"id":"class_id_2"}
    
    ]
}
print("\nBulk data\n")
result = bulk_get_data(db_url, document_ids)
if result:
    print(f"{result} \n")
else:
    print("Failed to fetch data.")

# HTTP Request using CURL
#curl -X POST http://admin:password@localhost:5984/students/_bulk_get -H "Accept: application/json" -H "Content-Type: application/json" -d "{\"docs\": [{\"id\": \"student_id_1\"}, {\"id\":\"student_id_5\"},{\"id\": \"teacher_id_3\"},{\"id\":\"class_id_2\"}]}"