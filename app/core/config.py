import os
import stripe
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(".env")

def require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# 🔐 ALL values come strictly from .env
STRIPE_SECRET_KEY = require_env("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = require_env("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = require_env("STRIPE_WEBHOOK_SECRET")
PRICE = require_env("PRICE")
DOMAIN = require_env("DOMAIN")
STATIC_DIR = require_env("STATIC_DIR")


# Stripe initialization (ONLY HERE)
stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = "2020-08-27"

stripe.set_app_info(
    "stripe-samples/checkout-one-time-payments",
    version="0.0.1"
)