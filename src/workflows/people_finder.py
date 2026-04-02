from pydantic import BaseModel, Field

from src.exa.exa_search import search_people_by_tech_stack
from src.exa.models import PersonSearchResult


class PeopleFinderConfig(BaseModel):
    """Configuration for people finder workflow."""

    max_iterations: int = Field(default=3, description="Maximum search iterations")
    results_per_search: int = Field(default=10, description="Results to fetch per iteration")
    min_results: int = Field(default=20, description="Stop early if we reach this many results")


class PeopleFinder:
    """
    Workflow for finding people from a company with specific skills.

    Handles iterative searching with deduplication.
    """

    def __init__(
        self,
        company: str,
        tech_stack: str | list[str],
        config: PeopleFinderConfig | None = None,
    ):
        self.company = company
        self.tech_stack = tech_stack
        self.config = config or PeopleFinderConfig()
        self.results: list[PersonSearchResult] = []
        self._seen_people: set[str] = set()

    def run(self) -> list[PersonSearchResult]:
        """
        Execute the people finding workflow.

        Returns accumulated unique results.
        """
        for _ in range(self.config.max_iterations):
            new_results = self._search()

            if not new_results:
                break

            if len(self.results) >= self.config.min_results:
                break

        return self.results

    def _search(self) -> list[PersonSearchResult]:
        """Run a single search and accumulate unique results."""
        response = search_people_by_tech_stack(
            self.company,
            self.tech_stack,
            self.config.results_per_search,
            self._seen_people
            
        )

        new_results = []
        for result in response.results:
            name = self._get_name(result)
            if name and name not in self._seen_people:
                self._seen_people.add(name)
                self.results.append(result)
                new_results.append(result)

        return new_results

    def _get_name(self, result: PersonSearchResult) -> str | None:
        """Extract person name from result."""
        if result.entities:
            return result.entities[0].properties.name
        return None
