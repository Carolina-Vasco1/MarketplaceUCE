from fastapi import HTTPException, status

def require_roles(*allowed: str):
    def _check(user: dict):
        role = user.get("role")
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role. Required: {allowed}",
            )
        return user
    return _check
