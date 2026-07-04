from dataclasses import dataclass

from app.core.errors import AuthenticationError, ConflictError, NotFoundError
from app.core.security import hash_password, verify_password


@dataclass
class UserRecord:
    # Internal user shape used by this service layer.
    id: int
    full_name: str
    email: str
    password_hash: str


class AuthService:
    """Simple auth service stored in memory for now."""

    def __init__(self) -> None:
        # Dictionary key is email, value is user record.
        self._users_by_email: dict[str, UserRecord] = {}
        # Very basic id counter for demo users.
        self._next_id = 1

    def register_user(self, full_name: str, email: str, password: str) -> UserRecord:
        # Normalize email so uppercase/lowercase versions are treated the same.
        normalized_email = email.strip().lower()
        if normalized_email in self._users_by_email:
            raise ConflictError("An account with this email already exists")

        user = UserRecord(
            id=self._next_id,
            full_name=full_name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
        )
        # Save user in memory and increment id for next registration.
        self._users_by_email[normalized_email] = user
        self._next_id += 1
        return user

    def authenticate_user(self, email: str, password: str) -> UserRecord:
        # Login succeeds only if user exists and password hash matches.
        normalized_email = email.strip().lower()
        user = self._users_by_email.get(normalized_email)
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Email or password is incorrect")
        return user

    def get_user_by_email(self, email: str) -> UserRecord:
        # Helper used by protected routes to load current user.
        normalized_email = email.strip().lower()
        user = self._users_by_email.get(normalized_email)
        if not user:
            raise NotFoundError("User not found")
        return user


# Shared singleton service for this scaffold app.
auth_service = AuthService()
