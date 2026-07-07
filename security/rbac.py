from fastapi import Depends, HTTPException
from security.auth import get_current_user


def require_permission(permission: str):
    def checker(current_user=Depends(get_current_user)):
        if "admin" in current_user["roles"]:
            return current_user

        if permission not in current_user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")

        return current_user

    return checker
