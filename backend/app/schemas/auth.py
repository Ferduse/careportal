from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    # Data we expect when a user creates a new account.
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    # Data we expect when a user logs in.
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class AuthTokenResponse(BaseModel):
    # Standard token response format used by many APIs.
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=10)


class LogoutRequest(BaseModel):
    refresh_token: str = Field(min_length=10)


class MessageResponse(BaseModel):
    message: str


class UserPublic(BaseModel):
    # Safe user fields we can return to the frontend.
    id: int
    full_name: str
    email: EmailStr
