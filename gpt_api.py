from openai import OpenAI
from constants import OPENAI_KEY
from parameters import reddit_prompts, newsletter_prompt, subreddits

def gpt_access():
    client = OpenAI(api_key=OPENAI_KEY)
    return client

def gpt_reddit(fetched_reddit_data):
    gpt_summaries = []
    client = gpt_access()
    for subreddit in subreddits:
        response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f'''{reddit_prompts[subreddit]}
                            \n
                            {fetched_reddit_data[subreddit]}
                        '''}
                    ],
                    model="gpt-4o",
                )
        summary = {subreddit : response.choices[0].message.content}
        gpt_summaries.append(summary)
        print(f"ChatGPT generated {subreddit} daily summary")
    return gpt_summaries