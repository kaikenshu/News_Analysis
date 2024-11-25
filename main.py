from Reddit_downloader import download_reddit
from mongo_manager import access_mongo, update_reddit_raw

if __name__ == "__main__":
    client = access_mongo()
    reddit_data = download_reddit()
    update_reddit_raw(client,reddit_data)