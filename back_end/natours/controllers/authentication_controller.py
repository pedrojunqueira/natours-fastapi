from datetime import datetime, timedelta
from typing import Optional, List
import uuid
import hashlib

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic.error_wrappers import ValidationError

from natours.config import settings
from natours.models.database import engine as db
from natours.models.security_model import TokenData
from natours.models.user_model import User
from natours.controllers.user_controller import select_user_keys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/token",
    scopes={"read": "read data about user", "write": "write data on users"},
)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def password_confirm_check(password, confirm_password):
    return password == confirm_password


async def authenticate_user(username: str, password: str):
    user = await db.find_one(User, User.username == username)
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
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await db.find_one(User, User.username == token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )


async def verify_non_existing_user(user):
    user_name = await db.find_one(User, User.username == user.username)
    if user_name:
        raise HTTPException(
            404, f"{user_name.username} already exist chose another one"
        )
    user_email = await db.find_one(User, User.email == user.email)
    if user_email:
        raise HTTPException(404, f"{user_email.email} already exist chose another one")
    return user


async def signup(user):
    if not password_confirm_check(user.password, user.confirm_password):
        raise HTTPException(404, f"password does not match")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    user.confirm_password = hashed_password
    user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        confirm_password=user.confirm_password,
        password_changed_at=datetime.now(),
        active=True,
    )
    user = await db.save(user)
    return user


def create_password_reset_token():
    return uuid.uuid4().hex


def hash_reset_token(token):
    hash_object = hashlib.sha256(token.encode())
    return hash_object.hexdigest()


async def check_existing_email(address):
    user = await db.find_one(User, User.email == address)
    return user


async def save_reset_password_token_to_db(address):
    user = await check_existing_email(address)

    if not user:
        raise HTTPException(404, f"email {address} not found")

    token = create_password_reset_token()

    user.password_reset_token = hash_reset_token(token)
    user.password_reset_expire = datetime.now() + timedelta(minutes=20)
    await db.save(user)

    return token


async def get_token_user(token):
    hashed_token = hash_reset_token(token)
    user = await db.find_one(
        User,
        (User.password_reset_token == hashed_token)
        and (datetime.now() < User.password_reset_expire),
    )
    if not user:
        raise HTTPException(404, f"token expired or not valid")

    return user


async def save_reset_password(user, passwords):
    if not password_confirm_check(passwords.password, passwords.confirm_password):
        raise HTTPException(404, f"password does not match")
    hashed_password = get_password_hash(passwords.password)
    user.password = hashed_password
    user.confirm_password = hashed_password
    user.password_reset_token = None
    user.password_reset_expire = None
    user.password_changed_at = datetime.now()
    user = await db.save(user)
    return user


async def save_updated_password(user, passwords):
    if not password_confirm_check(passwords.password, passwords.confirm_password):
        raise HTTPException(404, f"password does not match")
    hashed_password = get_password_hash(passwords.password)
    user.password = hashed_password
    user.confirm_password = hashed_password
    user.password_changed_at = datetime.now()
    user = await db.save(user)
    return user
