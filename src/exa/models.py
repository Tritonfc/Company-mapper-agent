from pydantic import BaseModel, Field, ConfigDict


class DateRange(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """Date range for work/education history."""

    from_date: str | None = Field(default=None, alias="from")
    to_date: str | None = Field(default=None, alias="to")


class Company(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """Company info from work history."""

    id: str | None = None
    name: str


class Institution(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """Educational institution."""

    id: str | None = None
    name: str


class WorkExperience(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """A single work experience entry."""

    title: str
    company: Company
    location: str | None = None
    dates: DateRange | None = None


class Education(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """A single education entry."""

    degree: str | None = None
    institution: Institution
    dates: DateRange | None = None


class PersonProperties(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes= True)  
    """Properties of a person profile."""

    name: str
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    location: str | None = None
    work_history: list[WorkExperience] | None = Field(default=None, alias="workHistory")
    education_history: list[Education] | None = Field(default=None, alias="educationHistory")


class PersonEntity(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """Entity containing person data."""

    id: str
    type: str
    properties: PersonProperties


class PersonSearchResult(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True, from_attributes=True)  
    """A single person result from Exa search."""

    id: str
    title: str
    url: str
    published_date: str | None 
    author: str | None = None
    image: str | None = None
    entities: list[PersonEntity] = Field(default_factory=list)


class ExaSearchResponse(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True,from_attributes=True)  
    """Full response from Exa people search."""
    resolved_search_type: str 
    results: list[PersonSearchResult]
    search_time: float 
