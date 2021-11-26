from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from natours.models.user_model import Users
from natours.models.security_model import TokenData
from natours.models.database import engine as db
from natours.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await db.find_one(Users, Users.username == username) 
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.find_one(Users, Users.username == token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def verify_non_existing_user(user):
    user_name = await db.find_one(Users, Users.username == user.username)
    if user_name:
        raise HTTPException(404, f"{user_name.username} already exist chose another one")
    user_email = await db.find_one(Users, Users.email == user.email)
    if user_email:
        raise HTTPException(404, f"{user_email.email} already exist chose another one")
    return user

async def signup(user):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.confirm_password = hashed_password
    user = Users(username = user.username,
                email = user.email,
                password = user.password,
                confirm_password = user.confirm_password
                )
    user = await db.save(user)
    return user.dict()