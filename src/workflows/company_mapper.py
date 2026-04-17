from typing import Any, Callable

import pandas as pd

from src.common.enums import ProgressStage
from src.data.transformers import to_dataframe
from src.github.client import GitHubClient
from src.workflows.models import VerificationResult
from src.workflows.people_finder import PeopleFinder
from src.workflows.tech_stack_verifier import TechStackVerifier
from src.exa.models import PersonSearchResult
from src.agent.models import CompanyResult


class CompanyMapperResult:
    """Result container for the full workflow."""

    def __init__(
        self,
        verified: list[VerificationResult],
        failed: list[VerificationResult],
        people: list[PersonSearchResult],
    ):
        self.verified = verified
        self.failed = failed
        self.people = people

    def verified_df(self) -> pd.DataFrame:
        """Companies confirmed to have the tech stack."""
        return to_dataframe(self.verified, {
            "Company": "company",
            "GitHub Org": "github_org",
            "Tech Stack": "tech",
            "Matching Repos": "matching_repos_count",
            "Status": "status",
        })

    def people_df(self) -> pd.DataFrame:
        """People found from companies."""
        return to_dataframe(self.people, {
            "Name": "entities.0.properties.name",
            "Current Company": "entities.0.properties.work_history.0.company.name",
            "Title": "entities.0.properties.work_history.0.title",
            "LinkedIn": "url",
            "Score": "pointScore",
        })


class CompanyMapper:
    """
    Orchestrates the full company mapping workflow.

    1. Verify which companies use the tech stack
    2. Find people from companies that couldn't be verified via GitHub
    """

    def __init__(self, job_role:str,location:str, on_progress: Callable[[ProgressStage, str|None, Any], None] | None = None):
        """
        Args:
            on_progress: Optional callback for progress updates.
                         Called with (stage: str, company: str, result: any)
        """
        self.on_progress = on_progress or (lambda *args: None)
        self.job_role = job_role
        self.location= location

    def run(self, companies: list[CompanyResult]) -> CompanyMapperResult:
        """
        Run the full workflow.

        Args:
            companies: List of CompanyResult models

        Returns:
            CompanyMapperResult with verified companies and people found
        """
        verified, failed = self._verify_companies(companies)
        # Combine the list to search for all occurences
        company_list = verified + failed
        people = self._find_people(company_list)
       

        return CompanyMapperResult(verified, failed, people)

    def _verify_companies(
        self, companies: list[CompanyResult]
    ) -> tuple[list[VerificationResult], list[VerificationResult]]:
        """Verify tech stack usage for all companies."""
        verified: list[VerificationResult] = []
        failed: list[VerificationResult] = []

        with GitHubClient() as client:
            verifier = TechStackVerifier(client)

            for company in companies:
                self.on_progress(ProgressStage.VERIFYING, company.name, None)

                result = verifier.verify(
                    company.name,
                    company.company_url,
                    company.tech,
                )

                self.on_progress(ProgressStage.VERIFIED, company.name, result)

                if result.status == "verified":
                    verified.append(result)
                else:
                    failed.append(result)

        return verified, failed

    def _find_people(
        self, companies: list[VerificationResult],
    ) -> list[PersonSearchResult]:
        """Find people from companies that failed verification."""
        all_people: list[PersonSearchResult] = []
        
        company_names = [company.company for company in companies]

        self.on_progress(ProgressStage.FINDING_PEOPLE, None, None)

        finder = PeopleFinder(companies= companies, tech_stack= companies[0].tech,job_role = self.job_role, location= self.location)
        people = finder.run()

        self.on_progress(ProgressStage.FOUND_PEOPLE, None, len(people))
        all_people.extend(people)

        return all_people
