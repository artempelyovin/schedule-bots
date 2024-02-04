from pydantic import BaseModel, ConfigDict, Field


class _OrmBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InstituteShortScheme(_OrmBaseModel):
    id: int = Field(description="ID института")
    short_name: str = Field(description="Аббревиатура института", examples=["ИИТиЭ"])


class InstituteDetailScheme(InstituteShortScheme):
    full_name: str = Field(
        description="Расшифровка аббревиатуры института",
        examples=["Институт информационных технологий и электроники"],
    )
    description: str = Field(
        description="Короткое описание института",
        examples=["Институт, созданный объединений двух других: ИПМФиИ и ИИТР"],
    )


class UniversityShortScheme(_OrmBaseModel):
    id: int = Field(description="ID университета")
    short_name: str = Field(description="Аббревиатура университета", examples=["ВлГУ"])


class UniversityDetailScheme(UniversityShortScheme):
    full_name: str = Field(
        description="Расшифровка аббревиатуры университета",
        examples=[
            "Владимирский государственный университет имени Александра Григорьевича и Николая Григорьевича Столетовых"
        ],
    )
    description: str = Field(
        description="Короткое описание института",
        examples=["один из ведущих вузов ЦФО, центр инновационного, технологического и социального развития региона."],
    )
    institutes: list[InstituteShortScheme] = Field(
        description="Список институтов, прикреплённых к данному университету"
    )
