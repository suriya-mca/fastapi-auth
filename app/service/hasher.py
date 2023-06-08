from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# password hash utility class
class Hasher():

    # function to verfify password
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:

        return pwd_context.verify(plain_password, hashed_password)
     

    # function to hash password
    @staticmethod
    def get_password_hash(password) -> str:

        return pwd_context.hash(password)
        