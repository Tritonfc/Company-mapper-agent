import os
from dotenv import load_dotenv
from exa_py import Exa

from .models import ExaSearchResponse, PersonSearchResult

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))


def search_people_by_tech_stack(
    company: str,
    tech_stack: str | list[str],
    num_results: int = 10,
    excluded_profiles : set[str]|None = None
) -> ExaSearchResponse:
    """
    Search for people from a company who use specific skills.

    Args:
        company: Company name to search within
        tech_stack: Technology or list of technologies (e.g., "React Native", ["Kotlin", "Swift"])
        num_results: Number of results to return

    Returns:
        ExaSearchResponse with people profiles
    """
    skills = [tech_stack] if isinstance(tech_stack, str) else tech_stack
    skills_str = ",".join(skills)
    
    
    base_query = f"Find me people from {company} who use these skills: {skills_str}"
    
    if not excluded_profiles:
         query = base_query
    else:
        excluded_str = ", ".join(excluded_profiles)   
        query = f"{base_query} and exclude these names: {excluded_str}"

   

    response = exa.search(
        query=query,
        type="neural",
        num_results=num_results,
        category="people",
        include_domains=["linkedin.com", "github.com"],
    )

    return ExaSearchResponse.model_validate({                                     
      "resolvedSearchType": response.resolved_search_type,                      
      "results": [r.__dict__ for r in response.results],                        
      "searchTime": response.search_time,                                       
  })     