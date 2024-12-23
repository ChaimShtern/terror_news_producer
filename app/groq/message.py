import json
from groq import Groq
import os

from dotenv import load_dotenv


load_dotenv(verbose=True)

client = Groq(
    api_key=os.environ['GROQ_API_KEY'],
)


def extract_location_details(title, content):
    clean_title = title.replace('\\', '')
    clean_content = content.replace('\\', '') if content else ''
    prompt = f"""
                Extract the location details (City, Country, Region) from the following news article.
                If no specific city, country, or region is mentioned, return None for the missing fields.
                Respond in this exact JSON format:
                {{
                    "city": ["city" or "null"],
                    "country": ["country" or "null"],
                     "region": ["region" or "null"]
                }}
                only one result for each and no additional comments at all
                and please dont use None!!


                News Message:
                "{clean_title, clean_content}"
                """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",
        )

        response = chat_completion.choices[0].message.content
        location_details = json.loads(response)

        return location_details

    except Exception as e:
        print(f"Error during location extraction: {e}")
        return None