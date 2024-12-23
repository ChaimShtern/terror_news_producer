from app.groq.message import extract_location_details
from app.repository.api_repo import fetch_articles


def general_service():
    keys = {'city', 'country', 'region'}
    news = fetch_articles()
    for new in news:
        location = extract_location_details(new['title'], new['body'])
        if location:
            location_keys = location.keys()
            if set(location_keys) == keys:
                return {**location, "date": new['date'], 'title': new['title']}
