from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse

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

# register router
app.include_router(authenticate.router)

# register tortoise orm
register_tortoise(  app,
                    config=DB_CONFIG,
                    generate_schemas=True,
                    add_exception_handlers=True
                )
