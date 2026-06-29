from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PermitRequest(BaseModel):
    project_name: str
    location: str

@app.get("/")
def read_root():
    return {"message": "PermitIQ backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/permits")
def create_permit(request: PermitRequest):
    return {
        "message": "Permit request received",
        "project_name": request.project_name,
        "location": request.location
    }

