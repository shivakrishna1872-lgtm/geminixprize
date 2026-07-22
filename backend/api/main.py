from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

app = FastAPI(title="AntiGravity Orchestrator API", version="1.0.0")

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
