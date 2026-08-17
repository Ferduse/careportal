from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.errors import AuthenticationError, ConflictError, NotFoundError
from app.core.security import hash_password, verify_password
from app.db.models import RefreshToken, User
from app.db.sql_queries import get_sql_query


UserRecord = User


class AuthService:
    """Auth service backed by the SQL database."""

    def register_user(self, db: Session, full_name: str, email: str, password: str) -> UserRecord:
        # Normalize email so uppercase/lowercase versions are treated the same.
        normalized_email = email.strip().lower()
        existing_user_stmt = select(User).from_statement(text(get_sql_query("get_user_by_email")))
        existing_user = db.scalar(existing_user_stmt, params={"email": normalized_email})
        if existing_user is not None:
            raise ConflictError("An account with this email already exists")

        user = User(
            full_name=full_name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> UserRecord:
        # Login succeeds only if user exists and password hash matches.
        normalized_email = email.strip().lower()
        user_stmt = select(User).from_statement(text(get_sql_query("get_user_by_email")))
        user = db.scalar(user_stmt, params={"email": normalized_email})
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Email or password is incorrect")
        return user

    def get_user_by_email(self, db: Session, email: str) -> UserRecord:
        # Helper used by protected routes to load current user.
        normalized_email = email.strip().lower()
        user_stmt = select(User).from_statement(text(get_sql_query("get_user_by_email")))
        user = db.scalar(user_stmt, params={"email": normalized_email})
        if not user:
            raise NotFoundError("User not found")
        return user

    def add_refresh_token(self, db: Session, token: str, user_id: int) -> None:
        db.add(RefreshToken(user_id=user_id, token=token))
        db.commit()

    def is_refresh_token_active(self, db: Session, token: str) -> bool:
        token_stmt = select(RefreshToken).from_statement(text(get_sql_query("get_refresh_token_by_token")))
        return db.scalar(token_stmt, params={"token": token}) is not None

    def revoke_refresh_token(self, db: Session, token: str) -> None:
        token_stmt = select(RefreshToken).from_statement(text(get_sql_query("get_refresh_token_by_token")))
        stored_token = db.scalar(token_stmt, params={"token": token})
        if stored_token is not None:
            db.delete(stored_token)
            db.commit()


# Shared singleton service for this scaffold app.
auth_service = AuthService()
