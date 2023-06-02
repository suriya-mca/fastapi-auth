from fastapi import APIRouter, HTTPException, status, Depends
from typing_extensions import Annotated

from model.models import UserInfo_Pydantic, UserInfoIn_Pydantic, UserInfo
from service.jwt.jwt_handler import signJWT, decodeJWT
from service.jwt.jwt_bearer import JWTBearer
from service.hasher import Hasher

router = APIRouter()


# test api
@router.get("/", dependencies=[Depends(JWTBearer())], tags=["test"])
def greet():
	return {"message": "hello"}


# post : user registration
@router.post("/api/auth/signup", tags=["register"])
async def register(userInfo: UserInfoIn_Pydantic):

	# check if user already exists
	if await UserInfo.get_or_none(email=userInfo.email) is not None:
		raise HTTPException(
	    	status_code = status.HTTP_400_BAD_REQUEST,
	    	detail = "User already exists"
        )

	hashed_password = Hasher.get_password_hash(userInfo.password)

	# save user
	await UserInfo.create(
		name = userInfo.name, 
		email = userInfo.email, 
		password = hashed_password
	)

	# create token
	token = signJWT(userInfo.email)

	return token


# get : verify email
@router.get("/api/auth/verify/", tags=["verify"])
async def email_verification(token: str):

	# decode token
	decoded_token = decodeJWT(token)

	if decoded_token is None:
		raise HTTPException(
			status_code = status.HTTP_401_UNAUTHORIZED,
			detail = "Token expired"
		)

	# update user model
	await UserInfo.filter(email = decoded_token["user_id"]).update(is_verified = True)

	return "Email verified"


# post : user login
@router.post("/api/auth/signin", tags=["login"])
async def login(userInfo: UserInfoIn_Pydantic):
	
	# get user info using user email
	user = await UserInfo_Pydantic.from_queryset_single(UserInfo.get(email = userInfo.email))

	# verify user email and password
	if user and Hasher.verify_password(userInfo.password, user.password) is False:
		raise HTTPException(
			status_code = status.HTTP_401_UNAUTHORIZED,
			detail = "Check your credintials."
		)
	return "Success!"
	

# get : forget password
@router.get("/api/auth/forget_password", tags=["forget password"])
async def forget_password(email: str):

	# check if user already exists
	if await UserInfo.get_or_none(email=email) is None:
		raise HTTPException(
	    	status_code = status.HTTP_400_BAD_REQUEST,
	    	detail = "User not exist"
        )

	# create token
	token = signJWT(email)

	return token


# put : change password
@router.put("/api/auth/change_password", tags=["change password"])
async def change_password(password: str, user_token: Annotated[UserInfoIn_Pydantic, Depends(JWTBearer())]):

	# decode token
	decoded_token = decodeJWT(user_token)
	# hash the new password
	hashed_password = Hasher.get_password_hash(password)

	# filter the user and change password
	user = await UserInfo.filter(email = decoded_token["user_id"]).update(password = hashed_password)

	return "password changed"


