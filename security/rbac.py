from fastapi import Depends, HTTPException


from security.auth import get_current_user


# Role Based Access Control (RBAC) DEPENDENCY
# =========================
def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=403, detail="Forbidden: insufficient permissions"
            )

        return user

    return role_checker
