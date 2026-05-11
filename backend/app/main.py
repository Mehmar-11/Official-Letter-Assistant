from fastapi import FastAPI

from app.routes.analysis import router as analysis_router


app = FastAPI(
    title="Official Letter Assistant API",
    description="Backend API for analyzing German official letters.",
    version="0.1.0",
)


app.include_router(analysis_router)


@app.get("/")
def read_root():
    return {"message": "Official Letter Assistant backend is running."}


@app.get("/health")
def health_check():
    return {"status": "ok"}