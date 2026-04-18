import os

import stripe
from core.config import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY




STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_CURRENCY = os.getenv("STRIPE_CURRENCY", "EUR")
STRIPE_COFFEE_AMOUNT = int(float(os.getenv("STRIPE_COFFEE_AMOUNT", "15.00")) * 100)  # Convert to cents
stripe.api_key = STRIPE_SECRET_KEY

def stripe_is_configured() -> bool:
    return bool(STRIPE_SECRET_KEY)

def create_coffee_checkout_session(
    success_url: str,
    cancel_url: str,
    amount: int,  #(in cents)
    customer_email: str,
):
    """
    Create a Stripe Checkout session with a custom amount.
    Amount must be in cents (e.g. 500 = €5.00)
    """

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        customer_email=customer_email,
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Wow you're buying Coffee ☕ for me?",},
                    "unit_amount": amount,  # dynamic amount
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return session