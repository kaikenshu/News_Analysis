from pymongo import MongoClient
from pymongo.server_api import ServerApi
from constants import MONGODB_URI
from parameters import subreddits


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
        collection = db['reddit_raw_test']
        for article_detail in reddit_data:
            collection.insert_one(article_detail)
        print(f"Inserted Reddit articles")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")

def flatten_comments(comments):
    return " | ".join([
        f"{comment.get('Comment', 'No Comment')} (Likes: {comment.get('Comment_Score', 0)})"
        for comment in comments
    ])

def fetch_reddit_raw(client):
    fetched_reddit_data = {}
    db = client['news']
    collection = db['reddit_raw']
    for subreddit in subreddits:
        # Fetch documents for the current subreddit
        documents = list(collection.find({'Subreddit': subreddit}))

        if not documents:
            print(f"No data found for subreddit: {subreddit}")
            continue

        # Flatten the data and prepare for CSV export
        flattened_data = []
        for doc in documents:
            flattened_doc = {
                'Created On': doc.get('Created On'),
                'Title': doc.get('Title'),
                'Score': doc.get('Score'),
                'Text': doc.get('Text'),
                'Comments': flatten_comments(doc.get('Comments', [])),  # Flatten the comments
            }
            flattened_data.append(flattened_doc)
        fetched_reddit_data[subreddit] = flattened_data
    return fetched_reddit_data

def update_reddit_summaries(client, gpt_summaries):
    try:
        db = client['news']
        collection = db['reddit_summaries_test']
        for summary in gpt_summaries:
            collection.insert_one(summary)
        print(f"Inserted Reddit articles")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")