from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import AuthenticationError
from app.core.security import decode_access_token
from app.services.auth_service import UserRecord, auth_service


# auto_error=False lets us return our own API error format.
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
