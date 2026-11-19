
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel


from data_onboarding.acl.acl import GroupName, UserContext
from data_onboarding.core import get_settings


settings = get_settings()
security = HTTPBearer

async def get_current_user_context(credentials: HTTPAuthorizationCredentials = Security(security)) -> UserContext:
    """Get the current user context from the authorization credentials."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.secrets.jwt_secret_key,
            algorithms=['HS256']
        )

        user_id: str = payload.get("sub")
        org_id: str = payload.get("org_id")
        raw_groups: list[str] = payload.get("groups", [])


        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

        return UserContext(
            user_id=user_id,
            org_id=org_id,
            groups=frozenset(GroupName(g) for g in raw_groups)
        )

    except jwt.PyJWKError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )