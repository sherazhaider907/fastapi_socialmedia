from pwdlib import PasswordHash

# Password hashing setup
password_hash = PasswordHash.recommended()

def hash(password: str) -> str:
    """Hash a password using pwdlib."""
    return password_hash.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return password_hash.verify(plain_password, hashed_password)