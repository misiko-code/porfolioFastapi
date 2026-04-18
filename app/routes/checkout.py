from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import STRIPE_PUBLISHABLE_KEY, DOMAIN
from services.stripe_service import (
    get_price,
    create_checkout_session,
    get_checkout_session
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/config")
async def get_config():
    price = get_price()
    return JSONResponse({
        "publicKey": STRIPE_PUBLISHABLE_KEY,
        "unitAmount": price["unit_amount"],
        "currency": price["currency"]
    })


@router.get("/checkout-session")
async def fetch_checkout_session(sessionId: str):
    session = get_checkout_session(sessionId)
    return JSONResponse(session)


@router.post("/create-checkout-session")
async def create_session(quantity: int = Form(1)):
    try:
        session = create_checkout_session(quantity, DOMAIN)
        return RedirectResponse(session.url, status_code=303)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/success")
async def success_page(request: Request, session_id: str):
    session = get_checkout_session(session_id)

    return templates.TemplateResponse("success.html", {
        "request": request,
        "session": session,
        "customer_email": session.get("customer_details", {}).get("email"),
        "amount_total": session.get("amount_total"),
        "currency": session.get("currency")
    })    