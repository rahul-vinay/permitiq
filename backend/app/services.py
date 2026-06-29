from fastapi import HTTPException
from backend.app.db import get_connection
from backend.app.schemas import PermitRequest, PermitResponse

def list_permits_service():
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

def get_permit_service(permit_id: int):
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

def create_permit_service(request: PermitRequest):
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

def delete_permit_service(permit_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM permits WHERE id = ?", (permit_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Permit not found")

    return {"message": f"Permit {permit_id} deleted successfully"}
