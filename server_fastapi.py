
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os
from dotenv import load_dotenv
load_dotenv()




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = os.getenv('DOMAIN')

# Define a model for the product data
class ProductInfo(BaseModel):
    product_name: str
    product_price: float
    currency: str = "usd"
    product_image: str = "https://i.imgur.com/EHyR2nP.png"
    product_description: str = ""

# API endpoint for JSON requests
@app.post("/create-checkout-session/api")
async def create_checkout_session_api(product_info: ProductInfo):
    try:
        unit_amount = int(product_info.product_price * 100)
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": product_info.currency,
                        "product_data": {
                            "name": product_info.product_name,
                            "images": [product_info.product_image],
                            "description": product_info.product_description,
                        },
                        "unit_amount": unit_amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Form endpoint for HTML form submissions  
@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    form_data = await request.form()
    
    try:
        product_name = form_data.get("product_name")
        product_price = float(form_data.get("product_price", 0))
        currency = form_data.get("currency", "usd")
        product_image = form_data.get("product_image", "https://i.imgur.com/EHyR2nP.png")
        product_description = form_data.get("product_description", "")
        
        # Convert price to cents
        unit_amount = int(product_price * 100)
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": product_name,
                            "images": [product_image],
                            "description": product_description,
                        },
                        "unit_amount": unit_amount,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
        return RedirectResponse(url=checkout_session.url, status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
