from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings


# bcrypt context used for password hashing and verification.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Convert plain password into a secure hash before storing it.
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check if login password matches the stored hash.
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    # Short-lived token used for protected API requests.
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "type": "access", "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str) -> str:
    # Longer-lived token used to get a new access token.
    expires_delta = timedelta(minutes=settings.refresh_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str:
    return _decode_token_subject(token, expected_type="access")


def decode_refresh_token(token: str) -> str:
    return _decode_token_subject(token, expected_type="refresh")


def _decode_token_subject(token: str, expected_type: str) -> str:
    try:
        # Decode token and check signature/expiration using our secret key.
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        token_type = payload.get("type")
        if token_type != expected_type:
            raise ValueError("Token type is invalid")
        subject = payload.get("sub")
        if not isinstance(subject, str):
            # We expect "sub" to contain a string identifier.
            raise ValueError("Token subject missing")
        return subject
    except (JWTError, ValueError) as exc:
        # Keep a simple message that auth router can turn into 401 response.
        raise ValueError("Token is invalid or expired") from exc
