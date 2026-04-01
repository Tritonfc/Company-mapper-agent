from datetime import datetime, timedelta
from enum import Enum

from .models import RepoSearchResults, Repository, Commit, PullRequest


class SignalStrength(Enum):
    STRONG = "strong"
    WEAK = "weak"
    NONE = "none"


class SignalDetector:
    """
    Detects signal strength from GitHub API responses.

    Used to determine if we have enough evidence to exit early (strong),
    should continue searching (weak), or have no evidence (none).
    """

    def __init__(
        self,
        min_repos_for_strong: int = 2,
        min_stars_for_strong: int = 50,
        min_active_repos_for_strong: int = 3,
        min_keyword_repos_for_strong: int = 3,
        min_recent_commits_for_strong: int = 10,
        min_recent_prs_for_strong: int = 3,
        recent_activity_days: int = 180,
    ):
        self.min_repos_for_strong = min_repos_for_strong
        self.min_stars_for_strong = min_stars_for_strong
        self.min_active_repos_for_strong = min_active_repos_for_strong
        self.min_keyword_repos_for_strong = min_keyword_repos_for_strong
        self.min_recent_commits_for_strong = min_recent_commits_for_strong
        self.min_recent_prs_for_strong = min_recent_prs_for_strong
        self.recent_activity_days = recent_activity_days

    def _is_recent(self, timestamp: str | None) -> bool:
        """Check if timestamp is within the recent activity window."""
        if not timestamp:
            return False
        try:
            date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            cutoff = datetime.now(date.tzinfo) - timedelta(days=self.recent_activity_days)
            return date > cutoff
        except (ValueError, TypeError):
            return False

    def _count_active_repos(self, repos: list[Repository]) -> int:
        """Count repos with recent push activity."""
        return sum(1 for repo in repos if self._is_recent(repo.pushed_at))

    def _count_starred_repos(self, repos: list[Repository]) -> int:
        """Count repos meeting the star threshold."""
        return sum(1 for repo in repos if repo.stargazers_count >= self.min_stars_for_strong)

    def evaluate_language_search(self, results: RepoSearchResults) -> SignalStrength:
        """
        Evaluate signal strength from language search results.

        Strong: >= min_repos AND (>= min_active OR any starred)
        Weak: Some repos but doesn't meet strong criteria
        None: Zero repos
        """
        if results.total_count == 0 or not results.items:
            return SignalStrength.NONE

        active_count = self._count_active_repos(results.items)
        starred_count = self._count_starred_repos(results.items)

        has_enough_repos = results.total_count >= self.min_repos_for_strong
        has_active_repos = active_count >= self.min_active_repos_for_strong
        has_starred_repos = starred_count >= 1

        if has_enough_repos and (has_active_repos or has_starred_repos):
            return SignalStrength.STRONG

        return SignalStrength.WEAK

    def evaluate_keyword_search(self, results: RepoSearchResults) -> SignalStrength:
        """
        Evaluate signal strength from keyword search results.

        Strong: >= min_keyword_repos AND at least one active
        Weak: Some repos but doesn't meet strong criteria
        None: Zero repos
        """
        if results.total_count == 0 or not results.items:
            return SignalStrength.NONE

        active_count = self._count_active_repos(results.items)

        has_enough_repos = results.total_count >= self.min_keyword_repos_for_strong
        has_activity = active_count >= 1

        if has_enough_repos and has_activity:
            return SignalStrength.STRONG

        return SignalStrength.WEAK

    def evaluate_repo_deep_dive(
        self,
        repo: Repository,
        commits: list[Commit] | None,
        prs: list[PullRequest] | None,
        target_tech: str,
    ) -> SignalStrength:
        """
        Evaluate signal strength from deep dive into a single repo.

        Strong if any of:
          - Target tech in repo topics
          - Repo's primary language matches target
          - Has recent commits
          - Has recent PRs
        """
        target_lower = target_tech.lower()

        # Check topics
        if target_lower in [t.lower() for t in repo.topics]:
            return SignalStrength.STRONG

        # Check primary language
        if repo.language and repo.language.lower() == target_lower:
            return SignalStrength.STRONG

        # Check recent commits
        if commits:
            recent_commits = [c for c in commits if self._is_recent(c.commit.author.date)]
            if len(recent_commits) >= self.min_recent_commits_for_strong:
                return SignalStrength.STRONG

        # Check recent PRs
        if prs:
            recent_prs = [p for p in prs if self._is_recent(p.updated_at)]
            if len(recent_prs) >= self.min_recent_prs_for_strong:
                return SignalStrength.STRONG

        return SignalStrength.WEAK
