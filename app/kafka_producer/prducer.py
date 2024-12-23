import json
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

from app.service.general import general_service

load_dotenv(verbose=True)

elastic_topik = os.environ['ELASTIC_TOPIC']


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if hasattr(obj, '__dict__'):  # For pycountry objects and similar
            return str(obj)
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


producer = KafkaProducer(
    bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
    value_serializer=lambda v: json.dumps(v, cls=CustomJSONEncoder).encode()
)


def produce(topic: str, value):
    producer.send(
        topic=topic,
        value=value
    )


def sanitize_data(obj):
    if isinstance(obj, dict):
        return {k: sanitize_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_data(item) for item in obj]
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, '__dict__'):  # For pycountry objects
        return str(obj)
    return obj


def produce_elastic_news_messages(page):
    res = general_service(page)
    # Sanitize data before sending
    sanitized_fields = sanitize_data(res)

    produce(
        topic=elastic_topik,
        value=sanitized_fields
    )
