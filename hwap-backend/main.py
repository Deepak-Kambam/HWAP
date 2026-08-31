"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.session import init_db
from routers import auth, handshake, comms, signing, audit, system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB on startup."""
    init_db()
    yield


app = FastAPI(title="QUANTA Backend API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.auth_router)
app.include_router(auth.keys_router)
app.include_router(handshake.router)
app.include_router(comms.router)
app.include_router(signing.router)
app.include_router(audit.router)
app.include_router(system.router)
