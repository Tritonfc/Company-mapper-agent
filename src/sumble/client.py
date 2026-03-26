import os
import httpx

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