from fastapi import Depends, HTTPException
from security.auth import get_current_user


def require_permission(permission: str):
    def wrapper(current_user=Depends(get_current_user)):
        if current_user["role"] == "admin":
            return current_user

        permissions = current_user.get("permissions", [])

        if permission not in permissions:
            raise HTTPException(status_code=403, detail="Permission denied")

        return current_user

    return wrapper
