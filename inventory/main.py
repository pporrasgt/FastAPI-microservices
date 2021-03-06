from ctypes import cast
from itertools import product
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from decouple import config
from unipath import Path


BASE_DIR = Path(__file__).parent

HOST = config('HOST')
PORT = config('PORT')
PASSWORD = config('PASSWORD')
DECODE_RESPONSES = config("DECODE_RESPONSES")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=config('HOST', cast=str),
    port=config('PORT', cast=int),
    password=config('PASSWORD', cast=str),
    decode_responses=config("DECODE_RESPONSES", cast=bool)
)

class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    class Meta:
        database = redis

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return{
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity_available': product.quantity_available
    }

@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
