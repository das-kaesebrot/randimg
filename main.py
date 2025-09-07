from typing import Union

from fastapi import FastAPI
from api.cache import Cache

app = FastAPI(root_path="/api/v1")
cache = Cache("assets/images")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/img/{image_id}")
async def get_image(image_id: str, width: Union[int, None] = None, height: Union[int, None] = None):
    image = cache.get(image_id)
    pass


@app.get("/img")
async def get_rand_image(img_hash: str, width: Union[int, None] = None, height: Union[int, None] = None):
    pass
