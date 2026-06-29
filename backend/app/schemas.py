from pydantic import BaseModel

class PermitRequest(BaseModel):
    project_name: str
    location: str
