from fastapi import APIRouter, HTTPException, status, Depends
from typing_extensions import Annotated
from fastapi.security import APIKeyCookie
from starlette.responses import Response
from fastapi import BackgroundTasks

from model.models import UserInfo_Pydantic, UserInfoIn_Pydantic, UserInfo
from service.jwt.jwt_handler import signJWT, decodeJWT
from service.jwt.jwt_bearer import JWTBearer
from service.hasher import Hasher
from service.email import send_mail

# router instance
router = APIRouter()

# cookie instance
cookie_sec = APIKeyCookie(name="session")


# helper service: get current user
async def get_current_user(session: str = Depends(cookie_sec)):

	try:
		decoded_token: str = decodeJWT(session)
		user: str = decoded_token["user_id"]
		return user
	except Exception:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
		)


# get: get user
@router.get("/", tags=["test"])
async def get_user(username: str = Depends(get_current_user)):
	return {"message": username}


# post : user registration
@router.post("/api/auth/signup", tags=["register"])
async def register(userInfo: UserInfoIn_Pydantic, background_tasks: BackgroundTasks):

	# check if user already exists
	if await UserInfo.get_or_none(email=userInfo.email) is not None:
		raise HTTPException(
	    	status_code = status.HTTP_400_BAD_REQUEST,
	    	detail = "User already exists"
        )

	hashed_password: str = Hasher.get_password_hash(userInfo.password)

	# save user
	await UserInfo.create(
		name = userInfo.name, 
		email = userInfo.email, 
		password = hashed_password
	)

	# create token
	token: str = signJWT(userInfo.email, "register")

	# background task: send verification email
	verify_account = background_tasks.add_task(send_mail, userInfo.email, token)

	return {"message": "email has been sent"}


# get : verify email
@router.get("/api/auth/verify/", tags=["verify"])
async def email_verification(token: str):

	# decode token
	decoded_token: str = decodeJWT(token)

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
async def login(response: Response, userInfo: UserInfoIn_Pydantic):
	
	# get user info using user email
	user = await UserInfo_Pydantic.from_queryset_single(UserInfo.get(email = userInfo.email))

	# check the user is verified
	if user.is_verified:

		# verify user email and password
		if user and Hasher.verify_password(userInfo.password, user.password) is False:
			raise HTTPException(
				status_code = status.HTTP_401_UNAUTHORIZED,
				detail = "Check your credintials."
			)

		# create token
		token: str = signJWT(user.email, "login")

		# set cookie
		response.set_cookie("session", token)

		return "Success!"

	raise HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = "Verify your account"
	)
	

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
	token: str = signJWT(email, "password_change")

	return token


# put : change password
@router.put("/api/auth/change_password", tags=["change password"])
async def change_password(password: str, user_token: Annotated[UserInfoIn_Pydantic, Depends(JWTBearer())]):

	# decode token
	decoded_token: str = decodeJWT(user_token)

	user = await UserInfo_Pydantic.from_queryset_single(UserInfo.get(email = decoded_token["user_id"]))

	if Hasher.verify_password(password, user.password) is False:

		# hash the new password
		hashed_password: str = Hasher.get_password_hash(password)

		# filter the user and change password
		await UserInfo.filter(email = decoded_token["user_id"]).update(password = hashed_password)

		return "password changed"

	raise HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = "Don't use the old password"
	)


# get: logout
@router.get("/api/auth/logut", tags=["logout"])
async def logout(response: Response):

	# delete cookie
	response.delete_cookie("session")
	return {"message": "cookie deleted"}