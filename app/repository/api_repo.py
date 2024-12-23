import os
import requests
import time

# מפתח API
API_KEY = "ceedbd7a-61df-41fd-a695-fb512b2a5240"  # החלף במפתח האמיתי שלך

# כתובת ה-API
url = "https://eventregistry.org/api/v1/article/getArticles"

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
            print(f"Page {page} Data:", data)  # הדפסת תוצאות
        else:
            print(f"Error on page {page}: {response.status_code}, {response.text}")
            break

        # דילוג לעמוד הבא
        page += 1

        # המתנה של 2 דקות
        time.sleep(120)