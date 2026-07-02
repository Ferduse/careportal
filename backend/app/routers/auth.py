from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import AuthenticationError
from app.core.security import create_access_token, decode_access_token
from app.schemas.auth import AuthTokenResponse, UserLoginRequest, UserPublic, UserRegisterRequest
from app.services.auth_service import UserRecord, auth_service


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserRecord:
    if credentials is None:
        raise AuthenticationError("Authorization token is missing")

    try:
        email = decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise AuthenticationError(str(exc)) from exc

    return auth_service.get_user_by_email(email)


@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserRegisterRequest) -> UserPublic:
    user = auth_service.register_user(
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )
    return UserPublic(id=user.id, full_name=user.full_name, email=user.email)


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: UserLoginRequest) -> AuthTokenResponse:
    user = auth_service.authenticate_user(email=payload.email, password=payload.password)
    token = create_access_token(user.email)
    return AuthTokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
def me(current_user: UserRecord = Depends(get_current_user)) -> UserPublic:
    return UserPublic(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
    )
