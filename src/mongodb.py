from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if hosted elsewhere

# Select the database and collection
db = client['History']  # Replace 'your_database' with your database name
collection = db['Mess']

def save_history(text, trans):
    document = {
        "text": text,
        "translation": trans
    }

    collection.insert_one(document)