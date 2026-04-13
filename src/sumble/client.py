import os
import httpx

from src.sumble.models import JobSearchCriteria

BASE_URL = "https://api.sumble.com/v5"
token = os.getenv("SUMBLE_API_KEY")


def find_organizations(
    filters: dict | str,
    limit: int = 10,
    offset: int = 0,
    include_entity_details: bool = False,
    order_by_column: str | None = None,
    order_by_direction: str | None = None,
):
    """
    Find organizations matching the given filters.

    Args:
        filters: Technology filters, job functions, or projects (dict or query string)
        limit: Number of results (1-200, default 10)
        offset: Pagination offset (0-10000, default 0)
        include_entity_details: Include full entity details (costs more credits)
        order_by_column: Column to sort by
        order_by_direction: "ASC" or "DESC"
    """
   

    body = {
        "filters": filters,
        "limit": limit,
        "offset": offset,
        "include_entity_details": include_entity_details,
    }

    if order_by_column:
        body["order_by_column"] = order_by_column
    if order_by_direction:
        body["order_by_direction"] = order_by_direction

    response = httpx.post(
        url=f"{BASE_URL}/organizations/find",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=body,
    )
    response.raise_for_status()
    return response.json()


def search_companies(criteria: JobSearchCriteria, limit: int = 20) -> list[dict]:
    """
    Search for companies using JobSearchCriteria.

    Args:
        criteria: The search criteria with tech skills and country
        limit: Max number of results

    Returns:
        List of companies formatted for CompanyMapper:
        [{"name": str, "tech": list[str], "company_url": str}, ...]
    """
    query_filter = criteria.to_sumble_filter()  # Using simple filter instead of advanced query
    response = find_organizations(
        filters=query_filter,
        limit=limit,
        include_entity_details=True,
    )

    companies = []
    for org in response.get("organizations", []):
        companies.append({
            "name": org.get("name", ""),
            "tech": criteria.tech,
            "company_url": org.get("website", org.get("url", "")),
        })

    return companies