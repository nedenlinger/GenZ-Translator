
import tweepy
import openai
import time
import json
import os
from datetime import datetime, timedelta

openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

BOT_SCREEN_NAME = "4GenZ"
LAST_SEEN_FILE = "last_seen_id.txt"
TRANSLATIONS_FILE = "translations.json"

def load_last_seen_id():
    if os.path.isfile(LAST_SEEN_FILE):
        with open(LAST_SEEN_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_last_seen_id(last_seen_id):
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(str(last_seen_id))

def load_translations():
    if os.path.isfile(TRANSLATIONS_FILE):
        with open(TRANSLATIONS_FILE, "r") as f:
            return json.load(f)
    return []

def save_translations(translations):
    with open(TRANSLATIONS_FILE, "w") as f:
        json.dump(translations, f, indent=2)

def genz_translate(text):
    prompt = f"""Translate the following sentence into modern Gen Z slang. Make it casual, funny, and use emojis when appropriate. Keep the meaning, but make it sound like a TikTok-obsessed teen might say it.

Original: "{text}" """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response['choices'][0]['message']['content'].strip()

def check_mentions(last_seen_id):
    new_last_seen_id = last_seen_id
    translations = load_translations()

    mentions = api.mentions_timeline(since_id=last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        tweet_id = mention.id
        user = mention.user.screen_name
        text = mention.full_text.replace(f"@{BOT_SCREEN_NAME}", "").strip()

        print(f"Translating for @{user}: {text}")
        try:
            translated = genz_translate(text)
        except Exception as e:
            print(f"OpenAI error: {e}")
            translated = "Sorry, I can't translate right now. Try again later!"

        reply = f"Yo @{user}, here’s your Gen Z version: \n\n{translated}"
        try:
            reply_tweet = api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        except tweepy.TweepError as e:
            print(f"Twitter reply error: {e}")
            continue

        translations.append({
            "original_tweet_id": tweet_id,
            "user": user,
            "translated_text": translated,
            "reply_id": reply_tweet.id,
            "likes": 0
        })

        new_last_seen_id = max(new_last_seen_id or 0, tweet_id)

    save_translations(translations)
    return new_last_seen_id

def update_likes():
    translations = load_translations()
    changed = False
    for t in translations:
        try:
            tweet = api.get_status(t["reply_id"])
            if tweet.favorite_count != t["likes"]:
                t["likes"] = tweet.favorite_count
                changed = True
        except tweepy.TweepError as e:
            print(f"Error fetching tweet {t['reply_id']}: {e}")
    if changed:
        save_translations(translations)
    return translations

def post_top_translation():
    translations = update_likes()
    if not translations:
        print("No translations to post.")
        return

    top = max(translations, key=lambda x: x["likes"])
    if top["likes"] == 0:
        print("No liked translations yet.")
        return

    post_text = f"🔥 Trending Gen Z Translation by @{top['user']}:\n\n{top['translated_text']}\n\n#4GenZ #GenZTranslate"
    try:
        api.update_status(post_text)
        print("Posted top trending translation to timeline.")
    except tweepy.TweepError as e:
        print(f"Error posting top translation: {e}")

def main():
    last_seen_id = load_last_seen_id()
    next_hour_post = datetime.utcnow() + timedelta(hours=1)
    while True:
        try:
            last_seen_id = check_mentions(last_seen_id)
            save_last_seen_id(last_seen_id)
        except tweepy.TooManyRequests:
            print("Rate limit hit, sleeping for 15 minutes...")
            time.sleep(900)
            continue
        except Exception as e:
            print(f"Error in check_mentions: {e}")

        if datetime.utcnow() >= next_hour_post:
            try:
                post_top_translation()
            except Exception as e:
                print(f"Error posting top translation: {e}")
            next_hour_post = datetime.utcnow() + timedelta(hours=1)

        time.sleep(12)

if __name__ == "__main__":
    main()
