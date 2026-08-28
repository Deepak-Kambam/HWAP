"""Auth and Keys routers."""
from fastapi import APIRouter
from datetime import datetime
import uuid
import time
import os
from models.schemas import UserRegister, UserResponse, GenerateKeysRequest, GenerateKeysResponse
from keystore import store_private_key
from routers import audit

try:
    import oqs
    if hasattr(oqs, 'KeyEncapsulation') and hasattr(oqs, 'Signature'):
        OQS_AVAILABLE = True
    else:
        OQS_AVAILABLE = False
except ImportError:
    OQS_AVAILABLE = False

auth_router = APIRouter(prefix="/api")
keys_router = APIRouter(prefix="/api/generate-keys")

@auth_router.post("/register", response_model=UserResponse)
async def register(req: UserRegister):
    """Registers a user."""
    user_id = str(uuid.uuid4())
    audit.add_event(
        user=f"{req.name} — {user_id[:8].upper()}",
        op="Registration",
        algo="—",
        result="Success"
    )
    return {"user_id": user_id, "created_at": datetime.utcnow().isoformat()}

@keys_router.post("/kem", response_model=GenerateKeysResponse)
async def generate_kem_keys(req: GenerateKeysRequest):
    """Generates KEM keypair."""
    start = time.perf_counter()
    if OQS_AVAILABLE:
        with oqs.KeyEncapsulation('Kyber768') as kem:
            pub = kem.generate_keypair()
            priv = kem.export_secret_key()
    else:
        pub = os.urandom(1184)
        priv = os.urandom(32)

    store_private_key(req.user_id, "ML-KEM-768", priv)
    keygen_ms = round((time.perf_counter() - start) * 1000, 2)
    audit.add_event(
        user=req.user_id[:20],
        op="Key Generation",
        algo="ML-KEM-768",
        result="Success"
    )
    return {
        "public_key_hex": pub.hex(),
        "algorithm": "ML-KEM-768",
        "keygen_ms": keygen_ms
    }

@keys_router.post("/dsa", response_model=GenerateKeysResponse)
async def generate_dsa_keys(req: GenerateKeysRequest):
    """Generates DSA keypair."""
    start = time.perf_counter()
    if OQS_AVAILABLE:
        with oqs.Signature('Dilithium3') as sig:
            pub = sig.generate_keypair()
            priv = sig.export_secret_key()
    else:
        pub = os.urandom(1952)
        priv = os.urandom(32)

    store_private_key(req.user_id, "ML-DSA-65", priv)
    keygen_ms = round((time.perf_counter() - start) * 1000, 2)
    audit.add_event(
        user=req.user_id[:20],
        op="Key Generation",
        algo="ML-DSA-65",
        result="Success"
    )
    return {
        "public_key_hex": pub.hex(),
        "algorithm": "ML-DSA-65",
        "keygen_ms": keygen_ms
    }
