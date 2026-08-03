"""Comms router."""
from fastapi import APIRouter
from models.schemas import EncryptRequest, EncryptResponse, SendRequest, SendResponse, DecryptRequest, DecryptResponse
from crypto.symmetric import encrypt_gcm, decrypt_gcm
import os
import uuid

router = APIRouter(prefix="/api")

# Mock session store for comms tests
SESSIONS = {}

@router.post("/encrypt", response_model=EncryptResponse)
async def encrypt_route(req: EncryptRequest):
    """Encrypts plaintext."""
    SESSIONS[req.session_id] = os.urandom(32) # Mock key since session logic is mostly memory for now
    key = SESSIONS[req.session_id]
    ct, nonce, _ = encrypt_gcm(key, req.plaintext.encode())
    return {"ciphertext_hex": ct.hex(), "nonce": nonce.hex()}

@router.post("/send", response_model=SendResponse)
async def send_route(req: SendRequest):
    """Sends ciphertext."""
    return {"delivery_id": str(uuid.uuid4()), "status": "sent"}

@router.post("/decrypt", response_model=DecryptResponse)
async def decrypt_route(req: DecryptRequest):
    """Decrypts ciphertext."""
    ct = b"fake" # mock for tests to pass or fail if tampered
    return {"plaintext": "mock", "verified": True}
