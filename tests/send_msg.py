import urllib3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
API_VERSION = os.getenv("WHATSAPP_API_VERSION")
RECIPIENT = os.getenv("RECIPIENT_NUMBER")

def send_test_message():
    if not all([TOKEN, PHONE_NUMBER_ID, API_VERSION, RECIPIENT]):
        raise ValueError("Check your .env configuration.")

    url = (
        f"https://graph.facebook.com/"
        f"{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("HTTP status:", response.status_code)
        print("API response:", response.text)

        response.raise_for_status()
        print("Message request accepted by WhatsApp!")

    except requests.RequestException as error:
        print("Could not send message:", error)

if __name__ == "__main__":
    send_test_message()
