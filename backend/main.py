"""
Wiom Talent Intelligence Platform — FastAPI Backend
"""
import os
from dotenv import load_dotenv

# Load from centralized credentials file (no-op on Railway where env vars are injected)
load_dotenv(r'C:\credentials\.env')

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.routers import auth, bootstrap, assessment, manager, admin, ai

app = FastAPI(
    title="Wiom Talent Intelligence API",
    version="1.0.0",
    description="AI-powered org skill mapping and upskilling platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-in-production"),
    max_age=86400,  # 24 hours
    same_site="lax",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth routes (no prefix — /login, /logout, /auth/callback) ─────────────────
app.include_router(auth.router)

# ── API routes ─────────────────────────────────────────────────────────────────
app.include_router(bootstrap.router, prefix="/api/v1", tags=["bootstrap"])
app.include_router(assessment.router, prefix="/api/v1", tags=["assessment"])
app.include_router(manager.router, prefix="/api/v1", tags=["manager"])
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"])


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "wiom-talent", "version": "1.0.0"}


# ── Static frontend ─────────────────────────────────────────────────────────────
# IMPORTANT: StaticFiles mount must come LAST — it is a catch-all.
# Any route defined after this is unreachable.
import os as _os
_frontend_dir = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), "frontend")
if _os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
