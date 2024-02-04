from pydantic import BaseModel, ConfigDict, Field


class UniversityScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="ID университета")
    short_name: str = Field(description="Аббревиатура университета", examples=["МГУ"])
    full_name: str = Field(
        description="Расшифровка аббревиатуры университета", examples=["Московский государственный университет"]
    )
    description: str = Field(description="Короткое описание института", examples=["Один из главных престижных России"])
