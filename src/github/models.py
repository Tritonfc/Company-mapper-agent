from pydantic import BaseModel, Field


class RepoOwner(BaseModel):
    """Repository owner (user or organization)."""

    login: str
    id: int


class License(BaseModel):
    """Repository license information."""

    key: str
    name: str
    spdx_id: str | None = None
    url: str | None = None


class Repository(BaseModel):
    """A Repository information"""

    id: int
    name: str
    full_name: str = Field(description="Full name in format 'owner/repo'")
    owner: RepoOwner
    private: bool = False
    description: str | None = None
    language: str | None = Field(default=None, description="Primary programming language")
    stargazers_count: int = 0
    forks_count: int = 0
    watchers_count: int = 0
    open_issues_count: int = 0
    topics: list[str] = Field(default_factory=list)
    pushed_at: str | None = Field(default=None, description="ISO 8601 timestamp of last push")
    updated_at: str | None = None
    created_at: str | None = None
    archived: bool = False
    fork: bool = False
    default_branch: str = "main"
    size: int = Field(default=0, description="Repository size in KB")
    license: License | None = None
    visibility: str = "public"

    # Search-specific fields (None when from get_repository)
    score: float | None = Field(default=None, description="Search relevance score")


class RepoSearchResults(BaseModel):
    """Response from GitHub search repositories API."""

    total_count: int
    incomplete_results: bool = False
    items: list[Repository]


class CommitAuthor(BaseModel):
    """Git author/committer info (not GitHub user)."""

    name: str
    email: str
    date: str = Field(description="ISO 8601 timestamp")


class CommitDetail(BaseModel):
    """The commit data itself."""

    message: str
    author: CommitAuthor
    committer: CommitAuthor


class GitHubUser(BaseModel):
    """GitHub user associated with a commit."""

    login: str
    id: int


class Commit(BaseModel):
    """A single commit from GET /repos/{owner}/{repo}/commits."""

    sha: str
    commit: CommitDetail
    author: GitHubUser | None = None
    committer: GitHubUser | None = None


class Label(BaseModel):
    """Issue/PR label."""

    name: str
    color: str | None = None
    description: str | None = None


class Issue(BaseModel):
    """A single issue from GET /repos/{owner}/{repo}/issues."""

    id: int
    number: int
    title: str
    state: str = Field(description="'open' or 'closed'")
    user: GitHubUser | None = None
    body: str | None = None
    labels: list[Label] = Field(default_factory=list)
    comments: int = 0
    created_at: str
    updated_at: str
    closed_at: str | None = None


class PullRequest(BaseModel):
    """A single pull request from GET /repos/{owner}/{repo}/pulls."""

    id: int
    number: int
    title: str
    state: str = Field(description="'open' or 'closed'")
    user: GitHubUser | None = None
    body: str | None = None
    labels: list[Label] = Field(default_factory=list)
    created_at: str
    updated_at: str
    closed_at: str | None = None
    merged_at: str | None = None
    draft: bool = False
