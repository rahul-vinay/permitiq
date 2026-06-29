from fastapi import FastAPI
from backend.app.schemas import PermitRequest, PermitResponse
from backend.app.db import init_db, get_connection

app = FastAPI()

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
def list_permits():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, project_name, location, permit_type FROM permits")
    rows = cursor.fetchall()
    conn.close()

    return [
        PermitResponse(
            id=row["id"],
            message="Permit record",
            project_name=row["project_name"],
            location=row["location"],
            permit_type=row["permit_type"],
        )
        for row in rows
    ]

@app.post("/permits", response_model=PermitResponse)
def create_permit(request: PermitRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO permits (project_name, location, permit_type) VALUES (?, ?, ?)",
        (request.project_name, request.location, request.permit_type),
    )
    conn.commit()
    permit_id = cursor.lastrowid
    conn.close()

    return PermitResponse(
        id=permit_id,
        message="Permit request received",
        project_name=request.project_name,
        location=request.location,
        permit_type=request.permit_type,
    )
