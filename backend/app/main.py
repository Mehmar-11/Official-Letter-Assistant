from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router

app = FastAPI(
    title="Official Letter Assistant API",
    description="Backend API for analyzing German official letters.",
    version="0.1.0",
)

# ✅ CORS (IMPORTANT for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(analysis_router)


@app.get("/")
def read_root():
    return {"message": "Official Letter Assistant backend is running."}


@app.get("/health")
def health_check():
    return {"status": "ok"}