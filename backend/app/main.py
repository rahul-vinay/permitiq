from fastapi import FastAPI
from backend.app.schemas import PermitRequest, PermitResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PermitIQ backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/permits", response_model=PermitResponse)
def create_permit(request: PermitRequest):
    return PermitResponse(
        message="Permit request received",
        project_name=request.project_name,
        location=request.location
    )
