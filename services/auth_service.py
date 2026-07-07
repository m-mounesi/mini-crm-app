from datetime import datetime, timedelta, timezone

from models.refresh_token import RefreshTokenDB
from repositories.user_repository import UserRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from security.password import hash_password, verify_password
from security.jwt import create_access_token, create_refresh_token, decode_refresh_token
from core.logger import get_logger, get_error_logger

from services.rbac_service import RBACService


logger = get_logger("AuthService")
error_logger = get_error_logger()
rbac_service = RBACService()


class AuthService:
    def __init__(self):
        self.repo = UserRepository()
        self.refresh_repo = RefreshTokenRepository()

    def register(self, db, form_data):
        if self.repo.get_user(db, form_data["username"]):
            return None

        user_data = {
            "username": form_data["username"],
            "password": hash_password(form_data["password"]),
        }

        user = self.repo.create_user(db, user_data)
        return user

    def login(self, db, username, password):
        user = self.repo.get_user(db, username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        context = rbac_service.build_user_context(db, user.user_id)

        access_token = create_access_token(
            {
                "sub": user.username,
                "user_id": user.user_id,
                "roles": context["roles"],
                "permissions": context["permissions"],
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user.username,
                "user_id": user.user_id,
                "type": "refresh",
            }
        )

        logger.info(f"saving refresh token for user_id: {user.user_id} in DB")

        #   Create obj and save in DB with refresh_repo create method
        refresh_obj = RefreshTokenDB(
            user_id=user.user_id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        if self.refresh_repo.create(db, refresh_obj):
            logger.info(
                f"Refresh token saved for user_id: {user.user_id} successfully in db"
            )

        logger.info(f"User logged in successfully: {username}")

        return {"access_token": access_token, "refresh_token": refresh_token}

    def logout(self, db, refresh_token: str):
        logger.info("Logout attempt")

        token_obj = self.refresh_repo.get_by_token(db, refresh_token)

        if not token_obj:
            return False

        self.refresh_repo.revoke(db, refresh_token)
        logger.info("Refresh token revoked")

        return True

    def refresh_tokens(self, db, refresh_token: str):
        logger.info("Refresh token attempt")

        # 1 - Decode and verify the jwt refresh token
        payload = decode_refresh_token(refresh_token)
        logger.info(f"payload data {payload}")
        if payload is None:
            logger.warning("Invalid refresh token. cannot decode_refresh_token")
            return None

        # 2 - DB check for the refresh token
        db_token = self.refresh_repo.get_by_token(db, refresh_token)

        if not db_token or db_token.is_revoked:
            logger.warning("Refresh token not found or revoked")
            return None

        # 3 - Revoke the old refresh token
        self.refresh_repo.revoke(db, refresh_token)
        logger.info("Old refresh token revoked")

        # 4 - Generate new access and refresh tokens
        logger.info("Full_data from decoded refresh token: " + str(payload))
        logger.info(f" {payload['user_id']} ")
        logger.info(
            f"{payload['sub']} - {payload['user_id']} - {payload.get('role', 'user')}"
        )

        new_access = create_access_token(
            {
                "sub": payload["sub"],
                "user_id": payload["user_id"],
                "role": payload.get("role", "user"),
            }
        )
        logger.info(f"New access token created for user_id: {payload.get('user_id')}")

        logger.info(f"Creating new refresh token for user_id: {payload.get('user_id')}")
        new_refresh = create_refresh_token(
            {"sub": payload["sub"], "user_id": payload["user_id"]}
        )

        refresh_obj = RefreshTokenDB(
            user_id=payload["user_id"],
            token=new_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        self.refresh_repo.create(db, refresh_obj)
        logger.info("New access and refresh tokens created")

        return {"access_token": new_access, "refresh_token": new_refresh}
