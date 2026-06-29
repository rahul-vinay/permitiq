from fastapi import FastAPI, HTTPException
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

@app.get("/permits/{permit_id}", response_model=PermitResponse)
def get_permit(permit_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, project_name, location, permit_type FROM permits WHERE id = ?",
        (permit_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Permit not found")

    return PermitResponse(
        id=row["id"],
        message="Permit record",
        project_name=row["project_name"],
        location=row["location"],
        permit_type=row["permit_type"],
    )

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

@app.delete("/permits/{permit_id}")
def delete_permit(permit_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM permits WHERE id = ?", (permit_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Permit not found")

    return {"message": f"Permit {permit_id} deleted successfully"}
