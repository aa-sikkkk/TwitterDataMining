import json
import tweepy
from tweepy import OAuth2BearerHandler
from dotenv import load_dotenv, set_key
import os

def process_or_store(tweet):
    print(json.dumps(tweet, indent=4))

# Load environment variables from .env file
load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')
user_id = os.getenv('USER_ID')

# Authenticate using Bearer Token
auth = OAuth2BearerHandler(bearer_token)
client = tweepy.Client(bearer_token=bearer_token)

if not user_id:
    # Fetch and save the user ID
    user = client.get_user(username="your_twitter_handle")
    user_id = user.data.id
    # Update .env file with the user ID
    set_key('.env', 'USER_ID', str(user_id))
    print(f"User ID {user_id} saved to .env file.")

try:
    # Get recent tweets from your timeline
    response = client.get_home_timeline(max_results=10)
    for tweet in response.data:
        process_or_store(tweet)
except tweepy.TweepyException as e:
    print(f"Error fetching home timeline: {e}")

try:
    # Get friends (following)
    response = client.get_users_following(id=user_id, max_results=10)
    for user in response.data:
        process_or_store(user)
except tweepy.TweepyException as e:
    print(f"Error fetching friends: {e}")

try:
    # Get followers
    response = client.get_users_followers(id=user_id, max_results=10)
    for user in response.data:
        process_or_store(user)
except tweepy.TweepyException as e:
    print(f"Error fetching followers: {e}")

try:
    # Get tweets from user timeline
    response = client.get_users_tweets(id=user_id, max_results=10)
    for tweet in response.data:
        process_or_store(tweet)
except tweepy.TweepyException as e:
    print(f"Error fetching user timeline: {e}")
