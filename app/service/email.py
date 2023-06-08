from decouple import config
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


# mail configuration
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


async def send_mail(email: str, token: str):

    jwt_token: str = token

    html = f"""
        <p>Thanks for registering, Verify your mail by clicking the below link</p>
        <a href="http://localhost:8000/api/auth/verify/?token={jwt_token}">Click here</a>
        <p><b>Note: </b>This link will expires in 10 minutes.</p> 
    """

    message = MessageSchema(
        subject="Verify your account!",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
