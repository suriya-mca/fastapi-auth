from fastapi import APIRouter, HTTPException, status, Depends

from model.models import UserInfo_Pydantic, UserInfoIn_Pydantic, UserInfo
from services.jwt.jwt_handler import signJWT, decodeJWT
from services.jwt.jwt_bearer import JWTBearer
from services.hasher import Hasher
from services.email import send_mail

router = APIRouter()


# test api
@router.get("/", dependencies=[Depends(JWTBearer())], tags=["test"])
def greet():
	return {
		"message": "hello"
	}


# post : user registration
@router.post("/api/auth/signup", tags=["register"])
async def register(userInfo: UserInfoIn_Pydantic):

	if await UserInfo.get_or_none(email=userInfo.email) is not None:
		raise HTTPException(
	    	status_code=status.HTTP_400_BAD_REQUEST,
	    	detail="User already exists"
        )

	await UserInfo.create(
		name = userInfo.name, 
		email = userInfo.email, 
		password = Hasher.get_password_hash(userInfo.password)
	)

	token = signJWT(userInfo.email)

	return "Account Created!"


# post : user login
@router.post("/api/auth/signin", tags=["login"])
async def login(userInfo: UserInfoIn_Pydantic):
	
	user = await UserInfo_Pydantic.from_queryset_single(UserInfo.get(email = userInfo.email))

	if user and Hasher.verify_password(userInfo.password, user.password):
		return signJWT(userInfo.email)

	raise HTTPException(
	    status_code=status.HTTP_401_UNAUTHORIZED,
	    detail="Check your credintials."
	)
