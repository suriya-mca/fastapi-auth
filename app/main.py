from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware
from fastapi.responses import UJSONResponse
import re

from router.auth import authenticate

from tortoise.contrib.fastapi import register_tortoise
from config.db import DB_CONFIG
from model.models import *


# create fast-api instance
app = FastAPI(default_response_class=UJSONResponse)

# cors settings
origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path_1 = re.compile("/api/auth/register")
path_2 = re.compile("/api/auth/verify")
path_3 = re.compile("/api/auth/logout")

app.add_middleware( 
    CSRFMiddleware, 
    secret = config("SECRET"),
    exempt_urls = [path_1 ,path_2, path_3],
    sensitive_cookies = [authenticate.cookie_sec],
    header_name = "x-csrftoken"
)

# register tortoise orm
register_tortoise(  app,
                    config=DB_CONFIG,
                    generate_schemas=False,
                    add_exception_handlers=True
                )

# register router
app.include_router(
    authenticate.router,
    prefix="/api/auth"
)