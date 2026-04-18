import json
import stripe

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from core.config import STRIPE_WEBHOOK_SECRET

router = APIRouter()

@router.post("/webhook")
async def webhook_received(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=STRIPE_WEBHOOK_SECRET
            )
            data = event["data"]
            event_type = event["type"]
        else:
            request_data = json.loads(payload)
            data = request_data["data"]
            event_type = request_data["type"]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    print("event " + event_type)

    if event["type"] == "checkout.session.completed":
        print("🔔 Payment succeeded!")
        #Log the amount in your webhook handler to see the amount paid by the user
        session = event["data"]["object"]

        amount_total = session["amount_total"]  # in cents
        print("User paid:", amount_total / 100, "€")

    return JSONResponse({"status": "success"})