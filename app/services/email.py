from typing import List
from decouple import config
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


conf = ConnectionConfig(
    MAIL_USERNAME = config('MAIL_USERNAME'),
    MAIL_PASSWORD = config('MAIL_PASSWORD'),
    MAIL_FROM = config('MAIL_USERNAME'),
    MAIL_PORT = config('MAIL_PORT'),
    MAIL_SERVER = config('MAIL_SERVER'),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)


async def send_mail(email: str, token: str) -> JSONResponse:

    jwt_token = token

    html = f"""
        <p>Thanks for registering, Verify your mail by clicking the below email.</p>
        <a href="http://localhost:8000/api/auth/verify/?token={jwt_token}">Click here</a> 
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})