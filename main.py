from reddit_downloader import download_reddit
from mongo_manager import access_mongo, update_reddit_raw, fetch_reddit_raw, update_reddit_summaries
from gpt_api import gpt_reddit

if __name__ == "__main__":

#Establish MongoDB access
    client = access_mongo()

#Downloading daily Reddit data
    # reddit_data = download_reddit()
    # update_reddit_raw(client,reddit_data)

#Getting daily GPT Reddit summaries
    fetched_reddit_data = fetch_reddit_raw(client)
    gpt_summaries = gpt_reddit(fetched_reddit_data)
    update_reddit_summaries(client,gpt_summaries)
