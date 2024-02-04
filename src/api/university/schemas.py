from pydantic import BaseModel, ConfigDict


class UniversityScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_name: str
    full_name: str
    description: str
