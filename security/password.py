from argon2 import PasswordHasher


ph = PasswordHasher()


# HASH PASSWORD
# =========================
def hash_password(password: str):
    return ph.hash(password)


# VERIFY PASSWORD
# =========================
def verify_password(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False
