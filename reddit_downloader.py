from datetime import datetime, timezone
import praw
from praw.models import Comment
from zoneinfo import ZoneInfo
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import pytesseract
from parameters import subreddits
from constants import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_USER_NAME, REDDIT_USER_PASSWORD

# **Initialize Reddit Instance**
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USER_NAME,
    password=REDDIT_USER_PASSWORD
)

now_pst = datetime.now()
today_date = now_pst.strftime('%Y-%m-%d %H:%M:%S')

def extract_text_from_image(url):
    try:
        print(f"Attempting to download image from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        print(f"Image downloaded successfully from {url}")

        # Optional: Preprocess the image for better OCR results
        img = img.convert('L')  # Convert to grayscale
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image

        text = pytesseract.image_to_string(img, lang='eng')
        print(f"Extracted Text: {text.strip()}")
        return text.strip()
    except Exception as e:
        print(f"Error processing image from {url}: {e}")
        return ""

def is_image_url(url):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    return any(url.lower().endswith(ext) for ext in image_extensions)

def download_reddit():
    reddit_data = []
    for subreddit_name in subreddits:
        print(f"\nScraping subreddit: {subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=200):
            # Calculate the time since the post was created
            post_creation_time = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
            hours_since_posted = (datetime.now(timezone.utc) - post_creation_time).total_seconds() / 3600
            min_score = 30 * hours_since_posted

            # Skip articles that do not meet the score requirement
            if submission.score < min_score:
                print(f"Skipping post: {submission.title} (Score: {submission.score}, Minimum Required: {min_score})")
                continue

            # Determine if the post is a text post or an image post
            if submission.is_self:
                post_text = submission.selftext
                print(f"Text post found: {submission.title}")
            elif is_image_url(submission.url):
                print(f"Image post found: {submission.url}")
                post_text = extract_text_from_image(submission.url)
                if not post_text:
                    post_text = "[Image] Unable to extract text from image."
            else:
                post_text = submission.url
                print(f"Non-text, non-image post found: {submission.url}")

            article_detail = {
                'Date': today_date,
                'Created On': post_creation_time.strftime('%Y-%m-%d %H:%M:%S'),
                'Subreddit': subreddit_name,
                'Title': submission.title,
                'URL': submission.url,
                'Score': submission.score,
                'Text': post_text,
                'Comments': [],  # This will hold the top-level comments
            }

            # Iterate over top-level comments only
            submission.comments.replace_more(limit=0)  # Prevent MoreComments from loading
            comment_min_score = 3 * hours_since_posted
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, Comment) and top_level_comment.score > comment_min_score:
                    comment_dic = {
                        'Comment': top_level_comment.body,
                        'Comment_Score': top_level_comment.score
                    }
                    article_detail['Comments'].append(comment_dic)
                else:
                    # Skip comments not meeting the score threshold
                    print(
                        f"Skipping comment with score {top_level_comment.score} (Minimum Required: {comment_min_score})")
                    continue
            reddit_data.append(article_detail)
    return reddit_data
