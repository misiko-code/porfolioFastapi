from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import portfolio, checkout, webhook


app = FastAPI(title="Portfolio App")

BASE_DIR = Path(__file__).resolve().parent


try:
    from app.db.db import mongo_is_available, save_client_signup
except ModuleNotFoundError:
    from app.db.db import mongo_is_available, save_client_signup

try:
    from app.services.payments import create_coffee_checkout_session, stripe_is_configured
except ModuleNotFoundError:
    from app.services.payments import create_coffee_checkout_session, stripe_is_configured


# Serve CSS, JavaScript, and other static assets from the app directory.
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/photos", StaticFiles(directory=BASE_DIR / "static" / "photos"),name="photos")

# routers
app.include_router(portfolio.router)
app.include_router(checkout.router)
app.include_router(webhook.router)
