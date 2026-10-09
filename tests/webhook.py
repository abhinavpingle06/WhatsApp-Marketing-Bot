
import os
import hmac
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "my_test_verify_token")


@app.get("/webhook")
async def verify_webhook(request: Request):
    """Meta uses this endpoint to verify your webhook."""
    params = request.query_params

    if (
        params.get("hub.mode") == "subscribe"
        and hmac.compare_digest(
            params.get("hub.verify_token", ""),
            VERIFY_TOKEN
        )
    ):
        return int(params.get("hub.challenge", "0"))

    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_message(request: Request):
    """Meta sends incoming WhatsApp events here."""
    data = await request.json()
    print("Incoming WhatsApp event:")
    print(data)
    return {"status": "received"}