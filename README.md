
# 4GenZ Bot Setup Guide

## 🔧 What This Bot Does
- Monitors mentions of your bot on Twitter/X
- Translates tagged tweets into Gen Z slang using OpenAI
- Replies with a slangified version
- Every hour, auto-posts the most liked translation to the timeline

## 🧰 Requirements

- Python 3.8+
- Twitter/X Developer Account
- OpenAI API Key
- Optional: Railway, Render, or Replit for hosting

## 🔑 Environment Variables

Set the following in your environment (via `.env`, Railway/Render dashboard, or locally):

```
OPENAI_API_KEY=your_openai_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
```

## 🚀 How to Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python genz_translate_bot.py
```

## ☁️ How to Deploy on Railway or Render

1. Create new project
2. Upload all files or connect GitHub repo
3. Set environment variables in the dashboard
4. Railway: add a `Worker` with `python genz_translate_bot.py`
5. Deploy and you're live!

## ⏱ Frequency & Monetization

- Checks mentions every 12 seconds (safe for Essential access)
- Posts most-liked reply every hour
- Upgrade Twitter API to Elevated Access or Premium as you grow
- Monetize through X Premium ad revenue or brand deals once eligible

## ✨ Tips

- Post 1–2 original Gen Z tweets per day
- Use hashtags like #4GenZ #GenZTranslate
- Keep branding fun, visual, and emoji-rich
