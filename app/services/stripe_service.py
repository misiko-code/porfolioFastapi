import stripe
from core.config import PRICE, DOMAIN


def get_price():
    return stripe.Price.retrieve(PRICE)


def create_checkout_session(quantity: int, domain: str):
    return stripe.checkout.Session.create(
        #success_url=domain + '/success.html?session_id={CHECKOUT_SESSION_ID}',
        success_url = DOMAIN + "success?session_id={CHECKOUT_SESSION_ID}",
        mode='payment',
        line_items=[{
            'price': PRICE,
            'quantity': quantity,
        }]
    )


def get_checkout_session(session_id: str):
    return stripe.checkout.Session.retrieve(session_id)