from fastapi import FastAPI
from backend.app.schemas import PermitRequest, PermitResponse

app = FastAPI()

permits = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "PermitIQ backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/permits", response_model=list[PermitResponse])
def list_permits():
    return permits

@app.post("/permits", response_model=PermitResponse)
def create_permit(request: PermitRequest):
    global next_id

    permit = PermitResponse(
        id=next_id,
        message="Permit request received",
        project_name=request.project_name,
        location=request.location,
        permit_type=request.permit_type
    )

    permits.append(permit)
    next_id += 1
    return permit
