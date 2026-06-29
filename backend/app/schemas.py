from pydantic import BaseModel, Field

class PermitRequest(BaseModel):
    project_name: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)

class PermitResponse(BaseModel):
    message: str
    project_name: str
    location: str
