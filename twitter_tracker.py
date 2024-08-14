import os
import requests
import csv
import time

# 从环境变量中读取 Bearer Token 和 Telegram 配置
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# 验证必要的环境变量是否存在
if not bearer_token:
    raise ValueError("Twitter Bearer Token is not set in the environment variables.")
if not telegram_bot_token or not telegram_chat_id:
    raise ValueError("Telegram Bot Token or Chat ID is not set in the environment variables.")

# 创建请求头
def create_headers(bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    return headers

# 获取指定用户的最新推文
def get_latest_tweet(username):
    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{username}"
    headers = create_headers(bearer_token)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    return response.json()

# 发送消息到 Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.status_code} {response.text}")

# 检查新推文并通知
def check_new_tweets():
    with open('kol_list.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['twitter_link'].split("/")[-1]
            tweets = get_latest_tweet(username)
            for tweet in tweets.get('data', []):
                tweet_id = tweet['id']
                tweet_text = tweet['text']
                created_at = tweet['created_at']

                if created_at > last_checked_time:
                    message = f"新推文來自 {row['kol_name']}:\n原文: {tweet_text}"
                    send_telegram_message(message)

# 程序入口，设置最后检查时间
last_checked_time = time.time()
while True:
    check_new_tweets()
    time.sleep(60)  # 每分钟检查一次
