import json

import tweepy

with open("keys.json") as reader:
    keys = json.load(reader)

API_KEY = keys["api_key"]
API_KEY_SECRET = keys["api_key_secret"]

ACCESS_TOKEN = keys["access_token"]
ACCESS_TOKEN_SECRET = keys["access_token_secret"]

AUTH = tweepy.OAuth2AppHandler(API_KEY, API_KEY_SECRET)

API = tweepy.API(AUTH, wait_on_rate_limit=True)

MAX_WORKERS = 8