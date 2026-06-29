from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "PermitIQ backend is running"}

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
