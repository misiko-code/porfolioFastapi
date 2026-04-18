from fastapi import APIRouter, Request, Form,status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo.errors import PyMongoError
import stripe

from db.db import mongo_is_available, save_client_signup
from services.payments import (
    create_coffee_checkout_session,
    stripe_is_configured,
)

# ---------------------------
# Helpers
# ---------------------------

def build_signup_context(
    request: Request,
    success: bool = False,
    form_data: dict | None = None,
    error_message: str | None = None,
    payment_message: str | None = None,
):
    return {
        "request": request,
        "success": success,
        "form_data": form_data or {},
        "db_status": mongo_is_available(),
        "error_message": error_message,
        "stripe_ready": stripe_is_configured(),
        "payment_message": payment_message,
    }


# ---------------------------
# Pages
# ---------------------------

router = APIRouter()
templates = Jinja2Templates(directory="templates")
BLOG_ACCESS_OPTIONS = {"Blog + CV access", "Blog only"}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
            request=request,
            name= "index.html",
            context={
            "title": "Emmanuel's Portfolio",
            "description": ("Welcome to my portfolio! I'm a robotics "
                            "engineer with a passion for integrating"),
        }
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    support_status = request.query_params.get("support")
    payment_message = None

    if support_status == "success":
        payment_message = "Thanks for the coffee support. Payment completed successfully."
    elif support_status == "cancelled":
        payment_message = "Coffee checkout was cancelled. You can try again anytime."
    elif support_status == "unavailable":
        payment_message = "Stripe is not configured yet."

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context=build_signup_context(
            request=request,
            payment_message=payment_message,
        ),
    )

@router.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={
            "request": request,
            "member_name": "Member",
        },
    )

# ---------------------------
# Signup
# ---------------------------

@router.post("/signup", response_class=HTMLResponse)
async def signup_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    access_request: str = Form(...),
    extras_interest: str = Form("No extra for now"),
    notes: str = Form(""),
):
    form_data = {
        "full_name": full_name,
        "email": email,
        "access_request": access_request,
        "extras_interest": extras_interest,
        "notes": notes,
    }

    try:
        save_client_signup(form_data)
        success = True
        error_message = None
    except PyMongoError:
        success = False
        error_message = "Database unavailable. Please try again later."

    # grant blog access if applicable
    if success and access_request in BLOG_ACCESS_OPTIONS:
        return templates.TemplateResponse(
            "blog.html",
            {
                "request": request,
                "member_name": full_name,
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context= build_signup_context(
            request=request,
            success=success,
            form_data=form_data,
            error_message=error_message,
        ),
    )

# ---------------------------
# Stripe Checkout (Support Coffee)
# ---------------------------

@router.post("/support/checkout")
async def support_checkout(request: Request, email: str = Form(""), amount: int = Form(...)):

    if not stripe_is_configured():
        return RedirectResponse(
            url="/signup?support=unavailable",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    success_url = str(request.url_for("signup_page")) + "?support=success"
    cancel_url = str(request.url_for("signup_page")) + "?support=cancelled"
    amount_cents = int(amount * 100)

    if amount < 1 or amount > 5000:
        return RedirectResponse(
        url="/signup?support=invalid",
        status_code=303
    )


    try:
        session = create_coffee_checkout_session(
            success_url=success_url,
            cancel_url=cancel_url,
            amount=amount_cents,
            customer_email=email,
        )
    except stripe.StripeError:
        return RedirectResponse(
            url="/signup?support=unavailable",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url=session.url,
        status_code=status.HTTP_303_SEE_OTHER,
    )

# ---------------------------
# API (Optional)
# ---------------------------
@router.get("/api/projects")
async def get_projects():
    # Lightweight JSON endpoint in case the portfolio needs API-driven sections later.
    return {
        "projects": [
            {"title": "Robotics Integration", "status": "featured"},
            {"title": "Predictive Maintenance", "status": "featured"},
            {"title": "Industrial Automation", "status": "featured"},
        ]
    }
