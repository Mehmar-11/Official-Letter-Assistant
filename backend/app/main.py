from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router

app = FastAPI(
    title="Official Letter Assistant API",
    description="Backend API for analyzing German official letters.",
    version="0.1.0",
)

# ✅ CORS - Updated with all frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "http://localhost:3000",  # Alternative local
        "https://official-letter-assistant.vercel.app",  # Your production frontend
        "https://*.vercel.app",  # All Vercel deployments
        "https://official-letter-assistant-git-*.vercel.app",  # Preview deployments
        "https://official-letter-assistant-backend.onrender.com",  # Your backend itself
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Routes
app.include_router(analysis_router)


@app.get("/")
def read_root():
    return {"message": "Official Letter Assistant backend is running."}


@app.get("/health")
def health_check():
    return {"status": "ok"}
