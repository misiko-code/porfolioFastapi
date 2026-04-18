import os
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://misikoeng:%23Manu2396@iot-cluster.jkuukl6.mongodb.net/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "portfolioUser")

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=3000)
    return _client


def get_clients_collection():
    client = get_mongo_client()
    return client[MONGODB_DB_NAME]["clients"]


def save_client_signup(form_data: dict) -> str:
    collection = get_clients_collection()
    now = datetime.now(timezone.utc)
    email = form_data["email"].strip().lower()

    payload = {
        "full_name": form_data["full_name"].strip(),
        "email": email,
        "access_request": form_data["access_request"],
        "extras_interest": form_data["extras_interest"],
        "notes": form_data["notes"].strip(),
        "updated_at": now,
    }

    result = collection.update_one(
        {"email": email},
        {
            "$set": payload,
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )

    return "created" if result.upserted_id else "updated"


def mongo_is_available() -> bool:
    try:
        get_mongo_client().admin.command("ping")
        return True
    except PyMongoError:
        return False
