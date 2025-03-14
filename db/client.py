from pymongo import MongoClient

# Local
# db_client = MongoClient().local

#Remote
db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.hejws.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    ).test

