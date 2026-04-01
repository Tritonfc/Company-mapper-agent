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
    
    search = DuckDuckGoSearchResults(num_results=5, output_format="list").with_retry(
           retry_if_exception_type=(Exception,),  # Retry on any exception
    stop_after_attempt=3     
    )
    
    search_run = DuckDuckGoSearchRun().with_retry(
    retry_if_exception_type=(Exception,),  # Retry on any exception
    stop_after_attempt=3                   # Retry up to 3 times
)
    
    results = list(google_search(query, num_results=10))
    duck_results = search.invoke(query)
    if not duck_results:
        return "No results found."

    formatted = []
    for r in duck_results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        formatted.append(f"{title} - {link}\n{snippet}")

    return "\n\n".join(formatted)


