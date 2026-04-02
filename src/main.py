from src.data.transformers import to_dataframe
from src.github.client import GitHubClient
from src.workflows.models import VerificationResult
from src.workflows.people_finder import PeopleFinder
from src.workflows.tech_stack_verifier import TechStackVerifier
from src.exa.models import PersonSearchResult


def run_verification(companies: list[dict]) -> tuple[list[VerificationResult], list[VerificationResult]]:
    """
    Run tech stack verification for a list of companies.

    Args:
        companies: List of dicts with 'name', 'tech', and 'company_url' keys

    Returns:
        Tuple of (verified_results, failed_results)
    """
    verified: list[VerificationResult] = []
    failed: list[VerificationResult] = []

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

            if result.status == "verified":
                verified.append(result)
            else:
                failed.append(result)

    return verified, failed


def find_people_for_failed(failed_results: list[VerificationResult])->list[PersonSearchResult]:
    """
    Run people finder for companies that failed verification.

    Args:
        failed_results: List of failed verification results
    """
    for result in failed_results:
        print(f"\n{'='*50}")
        print(f"Finding people at: {result.company}")
        print(f"Tech: {result.tech}")
        print('='*50)

        finder = PeopleFinder(result.company, result.tech)
        people = finder.run()

        print(f"Found {len(people)} people")
        
    return people

      


if __name__ == "__main__":
    companies = [
        {"name": "S-ryhma", "tech": ["react native"], "company_url": "s-ryhma.fi"},
        # {"name": "Kesko Oyj Kauppiaat", "tech": ["react native"], "company_url": "kesko.fi"},
        # {"name": "Veikkaus", "tech": ["react native"], "company_url": "veikkaus.fi"},
        {"name": "Virta", "tech": ["kotlin"], "company_url": "https://www.virta.global"},
    ]

    verified, failed = run_verification(companies)
    if verified:
        verified_df = to_dataframe(verified,{
            "Company":"company"
        }
            
        )
        print(verified_df.head())

    print(f"\n\n{'='*50}")
    print(f"SUMMARY: {len(verified)} verified, {len(failed)} failed")
    print('='*50)

    if failed:
       people_in_companies =  find_people_for_failed(failed)
    
    if people_in_companies:
            people_df = to_dataframe(people_in_companies, {
                "Name": "entities.0.properties.name",
                "Title": "entities.0.properties.work_history.0.title",
                "URL": "url",
            })
            
            print(people_df.head())
