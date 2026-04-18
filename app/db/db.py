import os
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError

_client: MongoClient | None = None


# ---------------------------
# Config (loaded at runtime)
# ---------------------------

def get_settings():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "portfolioUser")

    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set in environment variables")

    return mongo_uri, db_name


# ---------------------------
# Connection
# ---------------------------

def get_mongo_client() -> MongoClient:
    global _client

    if _client is None:
        mongo_uri, _ = get_settings()
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)

    return _client


def get_clients_collection():
    client = get_mongo_client()
    _, db_name = get_settings()
    return client[db_name]["clients"]


# ---------------------------
# CRUD
# ---------------------------

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


# ---------------------------
# Health Check
# ---------------------------

def mongo_is_available() -> bool:
    try:
        get_mongo_client().admin.command("ping")
        return True
    except PyMongoError:
        return False