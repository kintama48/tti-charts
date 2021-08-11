import json
import sys
import tweepy
import os
import discord
import time

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

API_KEY = config["API_key"]
API_SECRET = config["API_secret"]
ACCESS_KEY = config["access_key"]
ACCESS_SECRET = config["access_secret"]
USER_TO_SNITCH = config["user_handle"]
DISCORD_BOT_TOKEN = config["token"]
charts_channel_id = config["charts_channel_id"]

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
user = api.get_user(screen_name=USER_TO_SNITCH)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print("Starting to fetch the last tweet from the " + USER_TO_SNITCH + " account")

    last_tweet = '0'

    while True:
        current_last_tweet = \
        api.user_timeline(screen_name=USER_TO_SNITCH, count=1, include_rts=False, tweet_mode='extended')[0]
        if (int(current_last_tweet.id_str) > int(last_tweet)) and (not current_last_tweet.full_text.startswith('RT')):
            last_tweet = current_last_tweet.id_str
            media_link = current_last_tweet.extended_entities["media"][0]["media_url_https"]
            text = current_last_tweet.full_text.split()
            text.pop()
            text = " ".join(text)
            media_embed = discord.Embed(color=0xffd500, description=f"@everyone\n**{text}**").set_image(url=media_link)
            await client.get_channel(charts_channel_id).send(embed=media_embed)
        time.sleep(10)

if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)

# This URL can be used to add the bot to your server. Copy and paste the URL into your browser,
# choose a server to invite the bot to, and click “Authorize”. You need manage server permissions to do so.
# https://discord.com/api/oauth2/authorize?client_id=874522982960218133&permissions=8&scope=bot
