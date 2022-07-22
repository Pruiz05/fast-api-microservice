from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8000',
        'http://localhost:8001'
    ],
    allow_methods=['*'],
    allow_headers=['*']
)

#  connect to redis db
redis = get_redis_connection(
    host="redis-12499.c16.us-east-1-2.ec2.cloud.redislabs.com",
    port=12499,
    password="0RrA3uq7MzXEbxcKwrNOIg5MkPxdmGta",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }


@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)


@app.post('/products')
def create(product: Product):
    return product.save()


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)


