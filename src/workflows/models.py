from pydantic import BaseModel, Field
from src.exa.models import PersonSearchResult
from src.github.models import Repository
from src.github.signal_detector import SignalStrength


class VerificationResult(BaseModel):
    """Result of tech stack verification."""

    company: str
    tech: list[str] = Field(default_factory=list)
    github_org: str | None = None
    status: str = Field(description="'verified', 'not_verified', 'not_found', 'ambiguous'")
    signal_strength: SignalStrength | None = None
    matching_repos_count: int = 0
    repos: list[Repository] = Field(default_factory=list)
    reason: str | None = None
    
    
    
class RankedPersonResult(PersonSearchResult):
    pointScore:float
