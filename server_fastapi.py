
# # from fastapi import FastAPI, HTTPException, Request
# # from fastapi.responses import RedirectResponse
# # from fastapi.staticfiles import StaticFiles
# # from pydantic import BaseModel
# # from fastapi.middleware.cors import CORSMiddleware
# # import stripe
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()

# # YOUR_DOMAIN = "https://server-x8m2.onrender.com"


# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Your Stripe secret key
# # stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# # # YOUR_DOMAIN=os.getenv('DOMAIN')

# # # Define a model for the product data
# # class ProductInfo(BaseModel):
# #     product_name: str
# #     product_price: float
# #     currency: str = "usd"
# #     product_image: str = "https://i.imgur.com/EHyR2nP.png"
# #     product_description: str = ""

# # # API endpoint for JSON requests
# # @app.post("/create-checkout-session/api")
# # async def create_checkout_session_api(product_info: ProductInfo):
# #     try:
# #         unit_amount = int(product_info.product_price * 100)
        
# #         checkout_session = stripe.checkout.Session.create(
# #             line_items=[
# #                 {
# #                     "price_data": {
# #                         "currency": product_info.currency,
# #                         "product_data": {
# #                             "name": product_info.product_name,
# #                             "images": [product_info.product_image],
# #                             "description": product_info.product_description,
# #                         },
# #                         "unit_amount": unit_amount,
# #                     },
# #                     'quantity': 1,
# #                 },
# #             ],
# #             mode='payment',
# #             success_url=f'{YOUR_DOMAIN}/success',
# #             cancel_url=f'{YOUR_DOMAIN}/cancel',
# #         )
# #         return {"checkout_url": checkout_session.url}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # @app.get("/success")
# # async def success(request: Request):
# #     return {'status' : 'request successfull'}

# # @app.get("/cancel")
# # async def success(request: Request):
# #     return {'status' : 'request failed'}
    
# # # Form endpoint for HTML form submissions  
# # @app.post("/create-checkout-session")
# # async def create_checkout_session(request: Request):
# #     form_data = await request.form()
    
# #     try:
# #         product_name = form_data.get("product_name")
# #         product_price = float(form_data.get("product_price", 0))
# #         currency = form_data.get("currency", "usd")
# #         product_image = form_data.get("product_image", "https://i.imgur.com/EHyR2nP.png")
# #         product_description = form_data.get("product_description", "")
        
# #         # Convert price to cents
# #         unit_amount = int(product_price * 100)
        
# #         checkout_session = stripe.checkout.Session.create(
# #             line_items=[
# #                 {
# #                     "price_data": {
# #                         "currency": currency,
# #                         "product_data": {
# #                             "name": product_name,
# #                             "images": [product_image],
# #                             "description": product_description,
# #                         },
# #                         "unit_amount": unit_amount,
# #                     },
# #                     'quantity': 1,
# #                 },
# #             ],
# #             mode='payment',
# #             success_url=YOUR_DOMAIN + '?success=true',
# #             cancel_url=YOUR_DOMAIN + '?canceled=true',
# #         )
# #         return RedirectResponse(url=checkout_session.url, status_code=303)
    
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


# import os
# import stripe
# import uvicorn
# from fastapi import FastAPI, Request, Header
# from pydantic import BaseModel
# from dotenv import load_dotenv
# load_dotenv()
# from firebase_admin import credentials, firestore, initialize_app
# import os
# from pprint import pprint

# # Initialize Firebase
# cred_path = os.getenv("CRED_PATH")
# cred = credentials.Certificate(cred_path)
# initialize_app(cred)
# db = firestore.client()

# app = FastAPI()

# class ProductInfo(BaseModel):
#     product_name: str
#     product_price: float
#     currency: str = "usd"
#     product_image: str = "https://i.imgur.com/EHyR2nP.png"
#     product_description: str = ""
#     user_id: str = ""
#     number_of_connects: int = 0

# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# # This is a terrible idea, only used for demo purposes!
# app.state.stripe_customer_id = None


# @app.get("/success")
# async def success(request: Request):
#     return {"status": "success"}


# @app.get("/cancel")
# async def cancel(request: Request):
#     return {"status": "cancel"}


# @app.post("/create-checkout-session")
# async def create_checkout_session(product_info: ProductInfo):
#     if not app.state.stripe_customer_id:
#         customer = stripe.Customer.create(
#             description="Demo customer",
#         )
#         app.state.stripe_customer_id = customer["id"]
 
#     unit_amount = int(product_info.product_price * 100)
        
#     checkout_session = stripe.checkout.Session.create(
#         customer=app.state.stripe_customer_id,
#         success_url="https://server-x8m2.onrender.com/success?session_id={CHECKOUT_SESSION_ID}",
#         cancel_url="https://server-x8m2.onrender.com/cancel",
#         payment_method_types=["card"],
#         mode="payment",
#         line_items=[{
#                     "price_data": {
#                         "currency": product_info.currency,
#                         "product_data": {
#                             "name": product_info.product_name,
#                             "images": [product_info.product_image],
#                             "description": product_info.product_description,
#                         },
#                         "unit_amount": unit_amount,
#                     },
#                     'quantity': 1,
#         }],
#         metadata={"user_id":product_info.user_id,"number_of_connects":product_info.number_of_connects},
#     )
#     return {"sessionId": checkout_session["id"], "url":checkout_session.url}


# @app.post("/create-portal-session")
# async def create_portal_session():
#     session = stripe.billing_portal.Session.create(
#         customer=app.state.stripe_customer_id,
#         return_url="https://server-x8m2.onrender.com"
#     )
#     return {"url": session.url}


# @app.post("/webhook")
# async def webhook_received(request: Request, stripe_signature: str = Header(None)):
#     webhook_secret = "whsec_MjdtxocKXMAnafmVg88rambUP7d9sKOg"
#     # webhook_secret = "whsec_dbc51a61bed928be0a6d60efce987c73198e5a18a72eba8d32b398373e47796"
#     data = await request.body()
#     print("this is data : ",data)
#     try:
#         event = stripe.Webhook.construct_event(
#             payload=data,
#             sig_header=stripe_signature,
#             secret=webhook_secret
#         )
#         print("this is event : ", event)
#         event_data = event['data']
#         print("this is event data : ",event_data)
#     except Exception as e:
#         return {"error": str(e)}

#     event_type = event['type']
#     if event_type == 'checkout.session.completed':
#         return {"status": "checkout session completed"}
#     elif event_type == 'payment_intent.succeeded':
#         session = event['data']['object']
#         handle_checkout_session(session)
#         return {"status": "invoice paid"}
#     elif event_type == 'invoice.payment_failed':
#         return {"status": "invoice payment failed"}
#     else:
#         return {"status": f'unhandled event: {event_type}'}

# def handle_checkout_session(session):
#     # Fulfill the purchase
#     print("this is session data : ", session)
#     customer_email = session.get('customer_email')
#     # product_name = session['display_items'][0]['custom']['name']
#     amount_total = session['amount_received']
#     amount = float(amount_total)/100
#     product_name = 'Connect Package'
#     receipt_email=session['receipt_email']


#     # Example: Update Firestore with the transaction
#     transaction_data = {
#         'email': receipt_email,
#         'product': product_name,
#         'amount': amount,
#         'timestamp': firestore.SERVER_TIMESTAMP,
#     }
#     db.collection('test_transactions').add(transaction_data)
        

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from datetime import datetime

import stripe
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client

# Load environment variables
load_dotenv()

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store Stripe customer ID in app state (for demo purposes)
app.state.stripe_customer_id = None

# ---------------------------- MODELS ----------------------------

class ProductInfo(BaseModel):
    product_name: str
    product_price: float
    currency: str = "usd"
    product_image: str = "https://i.imgur.com/EHyR2nP.png"
    product_description: str = ""
    user_id: str = ""
    number_of_connects: int = 0

# ---------------------------- ROUTES ----------------------------

@app.get("/success")
async def success():
    return {"status": "success"}

@app.get("/cancel")
async def cancel():
    return {"status": "cancel"}

@app.post("/create-checkout-session")
async def create_checkout_session(product_info: ProductInfo):
    # Create customer once (demo purpose only)
    if not app.state.stripe_customer_id:
        customer = stripe.Customer.create(description="Demo customer")
        app.state.stripe_customer_id = customer["id"]

    unit_amount = int(product_info.product_price * 100)

    checkout_session = stripe.checkout.Session.create(
        customer=app.state.stripe_customer_id,
        success_url="https://server-x8m2.onrender.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://server-x8m2.onrender.com/cancel",
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": product_info.currency,
                "product_data": {
                    "name": product_info.product_name,
                    "images": [product_info.product_image],
                    "description": product_info.product_description,
                },
                "unit_amount": unit_amount,
            },
            "quantity": 1,
        }],
        metadata={
            "user_id": product_info.user_id,
            "number_of_connects": product_info.number_of_connects,
        },
    )

    return {"sessionId": checkout_session["id"], "url": checkout_session.url}

@app.post("/create-portal-session")
async def create_portal_session():
    session = stripe.billing_portal.Session.create(
        customer=app.state.stripe_customer_id,
        return_url="https://server-x8m2.onrender.com"
    )
    return {"url": session.url}

@app.post("/webhook")
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        return {"error": str(e)}

    event_type = event['type']
    session = event['data']['object']

    if event_type == 'checkout.session.completed':
        return {"status": "checkout session completed"}
    elif event_type == 'payment_intent.succeeded':
        handle_checkout_session(session)
        return {"status": "invoice paid"}
    elif event_type == 'invoice.payment_failed':
        return {"status": "invoice payment failed"}
    else:
        return {"status": f"unhandled event: {event_type}"}

# ---------------------------- UTILITY ----------------------------

def handle_checkout_session(session):
    customer_email = session.get('customer_email')
    receipt_email = session.get('receipt_email')
    amount_total = session.get('amount_received', 0)
    amount = float(amount_total) / 100
    product_name = 'Connect Package'

    transaction_data = {
        'email': customer_email or receipt_email,
        'product': product_name,
        'amount': amount,
    }

    response = supabase.table("transactions").insert({"data": transaction_data, 'timestamp': datetime.now()}).execute()

# ---------------------------- ENTRY POINT ----------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
