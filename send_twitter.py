import os
import requests
import json
from requests_oauthlib import OAuth1

from dotenv import load_dotenv
load_dotenv()


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def post_tweet_thread(text, link):
    # Split the text into chunks that don't split words and are under 280 characters each
    chunk_size = 280
    words = text.split()
    chunks = []
    current_chunk = ''

    for word in words:
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += ' ' + word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    last_chunk = chunks[-1]

    # Append link to last chunk if there is room
    if len(last_chunk) + 50 + 2 <= chunk_size:
        last_chunk += '\n\n' + link
        chunks[-1] = last_chunk
    else:
        chunks.append(link)

    print("Chunks: ", chunks)

    # Post the tweets in the thread
    prev_tweet_id = None
    for i, chunk in enumerate(chunks):
        if i == 0:
            tweet_text = chunk
            tweet_data = {
                'text': tweet_text
            }
            response = send_tweet_request(tweet_data)
            prev_tweet_id = response['data']['id']
        else:
            reply_text = chunk
            reply_data = {
                'text': reply_text,
                'reply': {
                    'in_reply_to_tweet_id': str(prev_tweet_id)
                }
            }
            response = send_tweet_request(reply_data)
            prev_tweet_id = response['data']['id']


def send_tweet_request(data):
    url = 'https://api.twitter.com/2/tweets'
    auth = OAuth1(consumer_key, consumer_secret, access_token,
                  access_token_secret)
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(
            auth=auth, url=url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f'Error: {e}\nResponse content: {e.response.text}')
