import requests
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# === Twitter Bearer Token ===
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAG4%2F1AEAAAAAB%2BR8QuG%2Far%2B%2BAeB8SoxdF5s%2Fnt0%3DTPeYuva9RW2QSzAZRk5gpS0jVB65lhXi6swtdYS4rLIYW1x2nv'

def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

def search_tweets(query, max_results=50):
    url = 'https://api.twitter.com/2/tweets/search/recent'
    params = {
        'query': query,
        'max_results': min(max_results, 100),
        'tweet.fields': 'text'
    }
    response = requests.get(url, headers=create_headers(), params=params)
    if response.status_code != 200:
        print("Error:", response.json())
        return []
    return response.json().get("data", [])

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"

def main():
    query = input("Enter a topic or hashtag (e.g. AI, #Bitcoin): ").strip()
    tweets = search_tweets(query)
    results = []
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for tweet in tweets:
        text = tweet['text']
        sentiment = analyze_sentiment(text)
        counts[sentiment] += 1
        results.append({"Tweet": text, "Sentiment": sentiment})
        print(f"{sentiment} -> {text}")

    # Save to CSV and Excel
    df = pd.DataFrame(results)
    csv_name = f"twitter_sentiment_{query.replace('#','')}.csv"
    excel_name = f"twitter_sentiment_{query.replace('#','')}.xlsx"
    df.to_csv(csv_name, index=False)
    df.to_excel(excel_name, index=False)

    print(f"\nSaved results to: {csv_name} and {excel_name}")

    # Plot
    plt.bar(counts.keys(), counts.values(), color=['green', 'red', 'gray'])
    plt.title(f"Twitter Sentiment on: {query}")
    plt.ylabel("Number of Tweets")
    plt.show()

if __name__ == "__main__":
    main()