from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import  Request
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8000'
    ],
    allow_methods=['*'],
    allow_headers=['*']
)

#  this should be a different db
redis = get_redis_connection(
    host="redis-12499.c16.us-east-1-2.ec2.cloud.redislabs.com",
    port=12499,
    password="0RrA3uq7MzXEbxcKwrNOIg5MkPxdmGta",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database: redis


@app.post('/orders')
async def create(request: Request):  # id, quantity
    body = await request.json()
    
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    return req
