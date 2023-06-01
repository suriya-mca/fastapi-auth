from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):

        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Week password, Password should contain 1 upper-case, 1 numeric and 1 special character."
            )

        return pwd_context.hash(password)