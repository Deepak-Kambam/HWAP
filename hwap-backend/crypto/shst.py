"""SHST formatting."""
import secrets

def generate_shst_token() -> str:
    """Generates a random SHST token."""
    return f"hwap-shst-{secrets.token_hex(16)}"
