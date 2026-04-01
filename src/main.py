from src.github.client import GitHubClient
from src.github.signal_detector import SignalDetector
from src.workflows.tech_stack_verifier import TechStackVerifier


def run_verification(companies: list[dict]) -> None:
    """
    Run tech stack verification for a list of companies.

    Args:
        companies: List of dicts with 'name' and 'tech' keys
                   e.g., [{"name": "Wolt", "tech": ["kotlin", "swift"]}]
    """
    with GitHubClient() as client:
        verifier = TechStackVerifier(client)

        for company in companies:
            name = company["name"]
            tech = company["tech"]
            url = company["company_url"]

            print(f"\n{'='*50}")
            print(f"Verifying: {name}")
            print(f"Tech: {tech}")
            print('='*50)

            result = verifier.verify(name, url, tech)

            print(f"Status: {result.status}")
            print(f"GitHub Org: {result.github_org}")
            print(f"Signal Strength: {result.signal_strength}")
            print(f"Matching Repos: {result.matching_repos_count}")

            if result.repos:
                print("Top Repos:")
                for repo in result.repos[:5]:
                    print(f"  - {repo.name} ({repo.stargazers_count} stars)")

            if result.reason:
                print(f"Reason: {result.reason}")


if __name__ == "__main__":
    companies = [
        {"name": "S-ryhma", "tech": ["react native"], "company_url": "s-ryhma.fi"},
        {"name": "Kesko Oyj Kauppiaat", "tech": ["react native"], "company_url": "kesko.fi"},
        {"name": "Veikkaus", "tech": ["react native"], "company_url": "veikkaus.fi"},
        {"name": "Virta", "tech": ["kotlin"], "company_url": "https://www.virta.global"},
        
    ]

    run_verification(companies)
