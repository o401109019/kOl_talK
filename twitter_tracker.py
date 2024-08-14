import csv
import tweepy
import time
import requests

# 讀取 CSV 文件並生成 KOL 名單
kol_list = []
with open('kol_list.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    kol_list = [row for row in reader]

# 設定 Twitter API 憑證
auth = tweepy.OAuthHandler('API_KEY', 'API_SECRET')
auth.set_access_token('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')
api = tweepy.API(auth)

# Telegram Bot 設置
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=data)

def check_new_tweets():
    for kol in kol_list:
        username = kol['kol_name']
        tweets = api.user_timeline(screen_name=kol['twitter_link'].split("/")[-1], count=1, tweet_mode='extended')
        for tweet in tweets:
            if tweet.created_at > last_checked_time:
                translated_text = translate_tweet(tweet.full_text)
                message = f"新推文來自 {username}:\n原文: {tweet.full_text}\n翻譯: {translated_text}"
                send_telegram_message(message)

def translate_tweet(text):
    # 使用翻譯 API (例如 Google 翻譯 API) 將推文翻譯為繁體中文
    translated_text = google_translate_api(text, target_lang='zh-TW')
    return translated_text

last_checked_time = time.time()
while True:
    check_new_tweets()
    time.sleep(60)  # 每分鐘檢查一次
