from pydantic import BaseModel, Field


class GithubNameResult(BaseModel):
    """Result of searching for a company's GitHub account."""

    username: str | None = Field(
        description="The GitHub organization or username (e.g., 'anthropics'). None if not found or ambiguous."
    )
    status: str = Field(
        description="One of: 'found', 'not_found', 'ambiguous'"
    )
    reason: str | None = Field(
        default=None,
        description="Explanation when status is 'not_found' or 'ambiguous'"
    )     