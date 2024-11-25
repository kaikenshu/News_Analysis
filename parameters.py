#Subreddits
subreddits = [
    'Bitcoin',
    'dogecoin',
    # 'MachineLearning',
    # 'Artificial',
    # 'TechNews',
    # 'Economics',
    # 'FinancialNews',
    # 'Finance',
    # 'Business',
    # 'StockMarket',
    # 'WallStreetBets',
]

#Reddit prompts
reddit_prompts = {
    'Bitcoin': """You are a senior investment professional and I am a very sophisticated investor. The following list contains hottest threads of past 7 days from reddit. The more likes (a.k.a. scores) a comment has, the more weight should be given to it. Please review the file in its entirety and give me a deep analysis of the following:
- based on the data, what is the general sentiment of today?
- how has the sentiment been trending over the past 7 days?
- score the sentiment between -100 (most bearish) to 100 (most bullish)
- is there any good insights today? (good as in providing useful data, pointing out correlation between things, identifying potential risks, depicting convincing scenarios, etc.) If an item was already covered on a previous day, highlight a change if any, otherwise omit it.
- is there any noteworthy news about economics, technology, business, stock markets, or prominent figures comments today (such as Elon Musk, Michael Saylor, Tim Draper, Jack Dorsey, Cathie Wood, and Trump)? If an item is already covered on a previous day, but is picked up again today, only include updates if any.""",
    'dogecoin': """You are a senior investment professional and I am a very sophisticated investor. The following list contains hottest threads of upto past 7 days from reddit. The more likes (a.k.a. scores) a comment has, the more weight should be given to it. Please review the file in its entirety and give me a deep analysis of the following:
- based on the data, what is the general sentiment of today?
- how has the sentiment been trending over the past 7 days?
- score the sentiment between -100 (most bearish) to 100 (most bullish)
- is there any good insights today? (good as in providing useful data, pointing out correlation between things, identifying potential risks, depicting convincing scenarios, etc.) If an item was already covered on a previous day, highlight a change if any, otherwise omit it.
- is there any noteworthy news about economics, technology, business, stock markets, or prominent figures comments today (such as Elon Musk, Michael Saylor, Tim Draper, Jack Dorsey, Cathie Wood, and Trump)? If an item is already covered on a previous day, but is picked up again today, only include updates if any.""",
}

#Newsletter prompt
newsletter_prompt = "Generate a PDF newsletter using the following analysis, focusing on key takeaways. Only return the PDF URL."