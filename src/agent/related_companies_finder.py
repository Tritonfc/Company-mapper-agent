from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage

from .models import CompanyResult

load_dotenv()

model = init_chat_model("claude-haiku-4-5")

SKILL_PATH = Path(__file__).parent / "skills" / "find-related-companies" / "SKILL.md"
SYSTEM_PROMPT = SKILL_PATH.read_text()


# Internal model for structured output
class _CompaniesResponse(BaseModel):
    """Internal response wrapper."""
    companies: list[CompanyResult] = Field(
        description="List of companies that use the specified technologies"
    )


related_companies_agent = create_agent(
    model=model,
    tools=[],  # No tools needed - just use Claude's knowledge
    system_prompt=SystemMessage(content=SYSTEM_PROMPT),
    name="related_companies_finder",
    response_format=_CompaniesResponse,
    debug=True
)


def find_related_companies(
    companyHire:str,
    tech: list[str],
    location: str | None = None,
    limit: int = 10
) -> list[CompanyResult]:
    """
    Find companies that use the specified technologies.

    Args:
        tech: List of technologies to search for
        location: Optional geographic focus
        limit: Maximum number of companies to return

    Returns:
        List of CompanyResult models
    """
    tech_str = ", ".join(tech)

    prompt = f"Find {limit} companies that use these technologies: {tech_str} that will be a good place to hire for {companyHire}, please exclude{companyHire} from the list of companies"
    if location:
        prompt += f". Focus on companies in or near {location}."

    messages = [
        HumanMessage(content=prompt)
    ]

    response = related_companies_agent.invoke({"messages": messages}) # type: ignore

    result: _CompaniesResponse = response["structured_response"]

    # Return just the list, with tech filled in
    companies = []
    for company in result.companies[:limit]:
        companies.append(CompanyResult(
            name=company.name,
            tech=tech,
            company_url=company.company_url
        ))

    return companies


# if __name__ == "__main__":
#     tech_input = input("Enter technologies (comma-separated): ")
#     tech_list = [t.strip() for t in tech_input.split(",")]
#     location = input("Location (optional, press enter to skip): ").strip() or None

#     results = find_related_companies(tech_list, location)

#     print(f"\nFound {len(results)} companies:")
#     for company in results:
#         print(f"  - {company.name}: {company.company_url}")
