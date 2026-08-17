from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.core.errors import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.schemas.auth import (
    AuthTokenResponse,
    LogoutRequest,
    MessageResponse,
    RefreshTokenRequest,
    UserLoginRequest,
    UserPublic,
    UserRegisterRequest,
)
from app.services.auth_service import UserRecord, auth_service


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> UserPublic:
    # Create a new user account.
    user = auth_service.register_user(
        db=db,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )
    return UserPublic(id=user.id, full_name=user.full_name, email=user.email)


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> AuthTokenResponse:
    # Validate login info and return JWT token.
    user = auth_service.authenticate_user(db, email=payload.email, password=payload.password)
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    auth_service.add_refresh_token(db, refresh_token, user.id)
    return AuthTokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AuthTokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> AuthTokenResponse:
    if not auth_service.is_refresh_token_active(db, payload.refresh_token):
        raise AuthenticationError("Refresh token is invalid or logged out")

    try:
        email = decode_refresh_token(payload.refresh_token)
    except ValueError as exc:
        raise AuthenticationError(str(exc)) from exc

    # Rotate refresh token so old token cannot be reused.
    auth_service.revoke_refresh_token(db, payload.refresh_token)
    user = auth_service.get_user_by_email(db, email)
    new_access_token = create_access_token(email)
    new_refresh_token = create_refresh_token(email)
    auth_service.add_refresh_token(db, new_refresh_token, user.id)
    return AuthTokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(payload: LogoutRequest, db: Session = Depends(get_db)) -> MessageResponse:
    auth_service.revoke_refresh_token(db, payload.refresh_token)
    return MessageResponse(message="Logged out")


@router.get("/me", response_model=UserPublic)
def me(current_user: UserRecord = Depends(get_current_user)) -> UserPublic:
    # Protected route: returns user info from the validated token.
    return UserPublic(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
    )
