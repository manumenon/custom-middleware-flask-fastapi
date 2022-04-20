import time
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import uvicorn

TOKEN_AUTH_SERVICE_URL = "http://127.0.0.1:5001"


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None


app = FastAPI()


@app.middleware("http")
async def authorization(request: Request, call_next):
    """
        Middleware function for each service call
    :param request:
    :param call_next:
    :return:
    """
    try:
        start_time = time.time()
        endpoint = request.url.path
        request_service_call_time_diff = "NA"
        if endpoint not in ['/', '/docs', '/favicon.ico', '/openapi.json',
                            "/healthcheck"]:

            token = request.headers.get('Authorization', "").split(" ")[-1]

            if not token:
                return JSONResponse(status_code=401, content='Authorization failed')

            jwt_res = requests.post(TOKEN_AUTH_SERVICE_URL, json={"token": token})
            if jwt_res.status_code != 200:
                return JSONResponse(status_code=401, content='Authorization failed')

        response = await call_next(request)
        return response
    except HTTPException as error:
        return JSONResponse(status_code=error.status_code,
                            content=error.detail)
    except Exception:
        return JSONResponse(status_code=500, content="Error while performing user authentication")


@app.post("/items/")
async def create_item():
    return {}

@app.get("/")
async def root():
    return "success"


@app.get("/healthcheck")
async def healthcheck():
    return "success"

uvicorn.run(app, port=8000, host="127.0.0.1")
