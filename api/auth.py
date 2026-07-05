from fastapi import APIRouter, Depends, status, HTTPException
from core.database import get_db
from sqlalchemy.orm import Session
from repositories.refresh_token_repository import RefreshTokenRepository
from schemas.schema import SuccessResponse
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from core.logger import get_logger
from fastapi.security import OAuth2PasswordRequestForm
from security.rbac import require_role


router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger("auth")
error_logger = get_logger("error")
repo = UserRepository()
refresh_repo = RefreshTokenRepository()
service = AuthService()


# signup
# =========================
@router.post("/register", status_code=status.HTTP_201_CREATED)
def signup(
    signupform: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    username = signupform.username
    password = signupform.password

    logger.info(f"User registration attempt: {username}")

    form_data = {"username": f"{username}", "password": f"{password}"}

    create_result = service.register(db, form_data)

    if not create_result:
        error_logger.error(f"Failed to create user: {username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user"
        )
    logger.info(f"User created successfully: {username}")
    return SuccessResponse(
        status_code=201, message=f"User {signupform.username} created successfully"
    )


# LOGIN
# =========================
@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info(f"Login attempt for user: {form_data.username}")
    tokens = service.login(db, form_data.username, form_data.password)

    if not tokens:
        error_logger.error(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    logger.info(f"User logged in successfully: {form_data.username}")
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


# Logout
# =========================
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(refresh_token: str, db: Session = Depends(get_db)):
    logger.info("Logout attempt")

    success = service.logout(db, refresh_token)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid token")

    logger.info("User logged out successfully")

    return {"message": "Logged out successfully"}


# Admin Endpoints (Require admin role)
# =========================
@router.get("/admin")
def admin(current_user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome, admin access granted for {current_user['username']}!"}


# Refresh Token Endpoint
# =========================
@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    logger.info("Refresh token attempt")

    try:
        tokens = service.refresh_tokens(db, refresh_token)

        if not tokens:
            logger.warning("Invalid refresh token. cannot refresh_tokens")
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return tokens

    except Exception as e:
        logger.error(f"Error occurred while refreshing token: {repr(e)}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
