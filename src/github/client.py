import os
from typing import Optional
import httpx


class GitHubClient:
    """
    GitHub API client for investigating company GitHub profiles.

    Usage:
        client = GitHubClient()
        org_info = client.get_organization("woltapp")
        repos = client.search_repos_by_language("woltapp", "kotlin")
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> dict:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # Step 2: Verify org profile
    # GET /orgs/{org}
    def get_organization(self, org: str) -> Optional[dict]:
        """
        Fetches organization profile information.
        Returns org details like name, description, public_repos count, etc.
        Returns None if org doesn't exist (404).
        """
        try:
            response = self.client.get(f"/orgs/{org}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 2 (fallback): Check if it's a user instead of org
    # GET /users/{username}
    def get_user(self, username: str) -> Optional[dict]:
        """
        Fetches user profile information.
        Fallback when org lookup returns 404 - some companies use personal accounts.
        """
        try:
            response = self.client.get(f"/users/{username}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 3: Filter repositories by language
    # GET /search/repositories?q=org:{org}+language:{lang}
    def search_repos_by_language(self, org: str, language: str | list[str]) -> dict:
        """
        Searches for repositories in an org that use specific programming language(s).
        Returns matching repos with their details.

        Args:
            org: GitHub organization name
            language: Single language or list of languages (OR logic - matches any)

        Returns dict with:
            - total_count: number of matching repos
            - items: list of repo objects
        """
        if isinstance(language, list):
            languages_query = " ".join(f"language:{lang}" for lang in language)
        else:
            languages_query = f"language:{language}"

        try:
            response = self.client.get(
                "/search/repositories",
                params={"q": f"org:{org} {languages_query}"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise

    # Step 4: Keyword search in repositories
    # GET /search/repositories?q=org:{org}+{keyword}
    def search_repos_by_keyword(self, org: str, keyword: str | list[str]) -> dict:
        """
        Searches for repositories in an org matching keyword(s).
        Searches in repo name, description, and README.
        Useful for finding tools/frameworks that aren't languages (e.g., react-native, docker).

        Args:
            org: GitHub organization name
            keyword: Single keyword or list of keywords (OR logic - matches any)

        Returns dict with:
            - total_count: number of matching repos
            - items: list of repo objects
        """
        if isinstance(keyword, list):
            keywords_query = " ".join(keyword)
        else:
            keywords_query = keyword

        try:
            response = self.client.get(
                "/search/repositories",
                params={"q": f"org:{org} {keywords_query}"}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise

    # Step 5: Get specific repository details
    # GET /repos/{owner}/{repo}
    def get_repository(self, owner: str, repo: str) -> Optional[dict]:
        """
        Fetches detailed information about a specific repository.
        Returns full repo details including languages, stars, forks, etc.
        Returns None if repo doesn't exist (404).
        """
        try:
            response = self.client.get(f"/repos/{owner}/{repo}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 6: Get repository topics
    # GET /repos/{owner}/{repo}/topics
    def get_repo_topics(self, owner: str, repo: str) -> Optional[dict]:
        """
        Fetches topics/tags assigned to a repository.
        Topics are labels like ["machine-learning", "python", "api"].
        Returns None if repo doesn't exist (404).
        """
        try:
            response = self.client.get(f"/repos/{owner}/{repo}/topics")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 7: Check dependency files
    # GET /repos/{owner}/{repo}/contents/{path}
    def get_file_contents(self, owner: str, repo: str, path: str) -> Optional[dict]:
        """
        Fetches contents of a specific file in a repository.
        Use for checking dependency files like package.json, requirements.txt, etc.
        Content is returned base64 encoded.
        Returns None if file doesn't exist (404).
        """
        try:
            response = self.client.get(f"/repos/{owner}/{repo}/contents/{path}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 8: Check commits
    # GET /repos/{owner}/{repo}/commits
    def get_commits(self, owner: str, repo: str, per_page: Optional[int] = 30) -> Optional[list]:
        """
        Fetches commit history for a repository.
        Returns recent commits with author, message, and date.
        Useful for checking if repo is actively maintained.
        Returns None if repo doesn't exist (404).
        """
        try:
            response = self.client.get(
                f"/repos/{owner}/{repo}/commits",
                params={"per_page": per_page}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 9: Check issues
    # GET /repos/{owner}/{repo}/issues
    def get_issues(self, owner: str, repo: str, state: Optional[str] = "open", per_page: Optional[int] = 30) -> Optional[list]:
        """
        Fetches issues for a repository.
        State can be "open", "closed", or "all".
        Returns None if repo doesn't exist (404).
        """
        try:
            response = self.client.get(
                f"/repos/{owner}/{repo}/issues",
                params={"state": state, "per_page": per_page}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Step 9: Check pull requests
    # GET /repos/{owner}/{repo}/pulls
    def get_pull_requests(self, owner: str, repo: str, state: Optional[str] = "open", per_page: Optional[int] = 30) -> Optional[list]:
        """
        Fetches pull requests for a repository.
        State can be "open", "closed", or "all".
        Returns None if repo doesn't exist (404).
        """
        try:
            response = self.client.get(
                f"/repos/{owner}/{repo}/pulls",
                params={"state": state, "per_page": per_page}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def close(self):
        """Close the HTTP client connection."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
