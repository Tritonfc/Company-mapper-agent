from pydantic import BaseModel, Field


class JobSearchCriteria(BaseModel):
    """Search criteria for finding candidates via Sumble."""

    company: str = Field(description="Company name we are hiring for")
    job_role: str = Field(description="Job role/title we are looking for")
    country: str = Field(description="Country to filter candidates by")
    tech: list[str] = Field(
        default_factory=list,
        description="1-3 core technical skills extracted from job description"
    )

    def to_sumble_filter(self) -> dict:
        """Build simple Sumble filter from criteria."""
        clean_tech = [skill.lower().replace("/", " ").strip() for skill in self.tech]
        return {"technologies": clean_tech}

    def to_sumble_query(self) -> dict:
        """Build Sumble advanced query filter from criteria."""
        conditions = []

        for skill in self.tech:
            # Clean skill name: remove special chars, lowercase
            clean_skill = skill.lower().replace("/", " ").strip()
            conditions.append(f"technology EQ '{clean_skill}'")

        # TODO: Add location filter once we confirm the correct field name
        # if self.country:
        #     conditions.append(f"hiring_location EQ '{self.country}'")

        query = " AND ".join(conditions)
        return {"query": f"({query})"}
