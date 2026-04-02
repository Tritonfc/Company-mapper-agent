from pydantic import BaseModel, Field


class DateRange(BaseModel):
    """Date range for work/education history."""

    from_date: str | None = Field(default=None, alias="from")
    to_date: str | None = Field(default=None, alias="to")


class Company(BaseModel):
    """Company info from work history."""

    id: str | None = None
    name: str


class Institution(BaseModel):
    """Educational institution."""

    id: str | None = None
    name: str


class WorkExperience(BaseModel):
    """A single work experience entry."""

    title: str
    company: Company
    location: str | None = None
    dates: DateRange | None = None


class Education(BaseModel):
    """A single education entry."""

    degree: str | None = None
    institution: Institution
    dates: DateRange | None = None


class PersonProperties(BaseModel):
    """Properties of a person profile."""

    name: str
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    location: str | None = None
    work_history: list[WorkExperience] = Field(default_factory=list, alias="workHistory")
    education_history: list[Education] = Field(default_factory=list, alias="educationHistory")


class PersonEntity(BaseModel):
    """Entity containing person data."""

    id: str
    type: str
    properties: PersonProperties


class PersonSearchResult(BaseModel):
    """A single person result from Exa search."""

    id: str
    title: str
    url: str
    published_date: str | None = Field(default=None, alias="publishedDate")
    author: str | None = None
    image: str | None = None
    entities: list[PersonEntity] = Field(default_factory=list)


class ExaSearchResponse(BaseModel):
    """Full response from Exa people search."""
    resolved_search_type: str = Field(alias="resolvedSearchType")
    results: list[PersonSearchResult]
    search_time: float = Field(alias="searchTime")
