import time

from app.kafka_producer.prducer import produce_elastic_news_messages

if __name__ == '__main__':
    page = 1
    while True:
        produce_elastic_news_messages(page)
        time.sleep(120)
        page += 1
