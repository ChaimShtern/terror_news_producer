import os
import requests
import time
from dotenv import load_dotenv
import json

load_dotenv(verbose=True)

# מפתח API
API_KEY = os.environ['NEWS_API_KEY']

# כתובת ה-API
url = os.environ['NEWS_URL']

# משתנה להגדרת מגבלת הבקשות
LIMIT = 1  # מספר הבקשות המרבי (ניתן לשנות)


# פונקציה לשליחת בקשות
def fetch_articles():
    page = 1
    for request_count in range(LIMIT):  # מגבלת בקשות
        body = {
            "action": "getArticles",
            "keyword": "terror attack",
            "ignoreSourceGroupUri": "paywall/paywalled_sources",
            "articlesPage": page,
            "articlesCount": 100,
            "articlesSortBy": "socialScore",
            "articlesSortByAsc": False,
            "dataType": ["news", "pr"],
            "forceMaxDataTimeWindow": 31,
            "resultType": "articles",
            "apiKey": API_KEY
        }

        response = requests.post(url, json=body)

        if response.status_code == 200:
            data = response.json()
            return data['articles']['results']
        else:
            print(f"Error on page {page}: {response.status_code}, {response.text}")
            break
            # המתנה של 2 דקות
    time.sleep(120)
        # דילוג לעמוד הבא
    page += 1

