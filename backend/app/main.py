from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.routes.analysis import router as analysis_router
from app.services.llm_service import check_llm_config

app = FastAPI(
    title="Official Letter Assistant API",
    description="Backend API for analyzing German official letters.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(CORS_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)


@app.get("/")
def read_root():
    return {"message": "Official Letter Assistant backend is running."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ready")
def readiness_check():
    if not check_llm_config():
        raise HTTPException(
            status_code=503,
            detail="The language model service is not configured.",
        )
    return {"status": "ready"}
