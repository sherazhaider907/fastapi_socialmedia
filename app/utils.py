from pwdlib import PasswordHash

# Password hashing setup
password_hash = PasswordHash.recommended()

def hash(password: str) -> str:
    """Hash a password using pwdlib."""
    return password_hash.hash(password)