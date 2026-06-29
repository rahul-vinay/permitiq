from typing import Optional
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.schemas import PermitRequest, PermitResponse
from backend.app.db import init_db
from backend.app.services import (
    list_permits_service,
    get_permit_service,
    create_permit_service,
    delete_permit_service,
    update_permit_service,
)

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/permits", response_model=list[PermitResponse])
def list_permits(location: Optional[str] = None, permit_type: Optional[str] = None):
    return list_permits_service(location=location, permit_type=permit_type)

@app.get("/permits/{permit_id}", response_model=PermitResponse)
def get_permit(permit_id: int):
    return get_permit_service(permit_id)

@app.post("/permits", response_model=PermitResponse)
def create_permit(request: PermitRequest):
    return create_permit_service(request)

@app.put("/permits/{permit_id}", response_model=PermitResponse)
def update_permit(permit_id: int, request: PermitRequest):
    return update_permit_service(permit_id, request)

@app.delete("/permits/{permit_id}")
def delete_permit(permit_id: int):
    return delete_permit_service(permit_id)
