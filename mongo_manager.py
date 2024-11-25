from pymongo import MongoClient
from pymongo.server_api import ServerApi
from constants import MONGODB_URI


def access_mongo():
    try:
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        print("MongoDB connection established successfully.")
        return client

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def update_reddit_raw(client, reddit_data):
    try:
        db = client['news']
        collection = db['reddit_raw']
        for article_detail in reddit_data:
            collection.insert_one(article_detail)
        print(f"Inserted Reddit articles")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")


