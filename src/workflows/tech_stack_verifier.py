from src.agent.github_finder import find_company_github
from src.github.client import GitHubClient
from src.github.models import RepoSearchResults, Repository
from src.github.signal_detector import SignalDetector, SignalStrength
from src.workflows.models import VerificationResult


class TechStackVerifier:
    """
    Verifies if a company actively uses a specific technology.

    Pipeline flow:
        1. Find GitHub org → if not found, exit
        2. Search by language → if STRONG signal, exit verified
        3. Search by keyword → if STRONG signal, exit verified
        4. Deep dive top repos → if any STRONG signal, exit verified
        5. All failed → exit not_verified
    """

    def __init__(
        self,
        client: GitHubClient,
        detector: SignalDetector | None = None,
        max_deep_dive_repos: int = 5,
    ):
        self.client = client
        self.detector = detector or SignalDetector()
        self.max_deep_dive_repos = max_deep_dive_repos
        self.context: dict = {}

    def verify(self, company: str, company_url, tech: str | list[str]) -> VerificationResult:
        """Run the verification pipeline."""
        self.context = {
            "company": company,
            "tech": [tech] if isinstance(tech, str) else tech,
            "company_url": company_url
        }

        return (
            self._find_org()
            or self._search_by_language()
            or self._search_by_keyword()
            or self._deep_dive()
            or self._fail()
        )

    def _find_org(self) -> VerificationResult | None:
        """Step 1: Find the GitHub org."""
        result = find_company_github(self.context["company"], self.context["company_url"])

        if result.status != "found":
            return VerificationResult(
                company=self.context["company"],
                tech=self.context["tech"],
                status=result.status,
                reason=result.reason,
            )

        self.context["org"] = result.username
        return None

    def _search_by_language(self) -> VerificationResult | None:
        """Step 2: Search repos by language."""
        try:
            results = self.client.search_repos_by_language(
            self.context["org"],
            self.context["tech"],
            )
            self.context["language_results"] = results

            if self.detector.evaluate_language_search(results) == SignalStrength.STRONG:
                return self._success(results)

            return None
        except Exception:
            return None

    def _search_by_keyword(self) -> VerificationResult | None:
        """Step 3: Search repos by keyword."""
        results = self.client.search_repos_by_keyword(
            self.context["org"],
            self.context["tech"],
        )
        self.context["keyword_results"] = results

        if self.detector.evaluate_keyword_search(results) == SignalStrength.STRONG:
            return self._success(results)

        return None

    def _deep_dive(self) -> VerificationResult | None:
        """Step 4: Deep dive into top repos."""
        
        try:
            repos = self.context["keyword_results"].items[:self.max_deep_dive_repos]

            for repo in repos:
                commits = self.client.get_commits(self.context["org"], repo.name)
                prs = self.client.get_pull_requests(self.context["org"], repo.name, state="all")

            for tech in self.context["tech"]:
                signal = self.detector.evaluate_repo_deep_dive(repo, commits, prs, tech)
                if signal == SignalStrength.STRONG:
                    return self._success_single(repo)

            return None
        except Exception:
            return None

    def _success(self, results: RepoSearchResults) -> VerificationResult:
        """Build successful verification result."""
        return VerificationResult(
            company=self.context["company"],
            tech=self.context["tech"],
            github_org=self.context["org"],
            status="verified",
            signal_strength=SignalStrength.STRONG,
            matching_repos_count=results.total_count,
            repos=results.items,
        )

    def _success_single(self, repo: Repository) -> VerificationResult:
        """Build successful verification result for single repo."""
        return VerificationResult(
            company=self.context["company"],
            tech=self.context["tech"],
            github_org=self.context["org"],
            status="verified",
            signal_strength=SignalStrength.STRONG,
            matching_repos_count=1,
            repos=[repo],
        )

    def _fail(self) -> VerificationResult:
        """Build failed verification result."""
        return VerificationResult(
            company=self.context["company"],
            tech=self.context["tech"],
            github_org=self.context["org"],
            status="not_verified",
            signal_strength=SignalStrength.WEAK,
            matching_repos_count=self.context.get("keyword_results", RepoSearchResults(total_count=0, items=[])).total_count,
            reason="Insufficient evidence of active usage",
        )
