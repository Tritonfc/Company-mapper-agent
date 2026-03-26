from langchain.tools import tool
from googlesearch import search as google_search
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchResults


@tool
def web_search(query: str) -> str:
    """
    Search Google with advanced operators.

    Supports Google search syntax like:
    - site:github.com
    - intitle:, -intitle:
    - inurl:, -inurl:
    - "exact phrase"
    - OR, AND operators

    Args:
        query: The search query with optional operators

    Returns:
        Newline-separated list of URLs from search results
    """
    
    search = DuckDuckGoSearchResults(output_format="json")
    
    results = list(google_search(query, num_results=10))
    duck_results = search.invoke(query)
    if not duck_results:
        return "No results found."

    return "\n".join(duck_results)


