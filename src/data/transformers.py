from typing import Any, Callable
import pandas as pd
from pydantic import BaseModel


def to_dataframe(
    items: list[Any],
    columns: dict[str, str | Callable[[Any], Any]] | None = None,
) -> pd.DataFrame:
    """
    Convert a list of objects to a pandas DataFrame.

    Args:
        items: List of objects (Pydantic models, dicts, or any objects)
        columns: Optional mapping of column_name -> attribute_name or extractor function
                 If None, uses model_dump() for Pydantic or __dict__ for objects

    Examples:
        # Simple - auto extract all fields
        df = to_dataframe(results)

        # Custom columns with attribute names
        df = to_dataframe(results, {
            "Name": "title",
            "URL": "url",
        })

        # Custom columns with extractor functions
        df = to_dataframe(results, {
            "Name": "title",
            "Company": lambda x: x.entities[0].properties.work_history[0].company.name,
        })
    """
    if not items:
        return pd.DataFrame()

    if columns is None:
        # Auto-extract all fields
        rows = []
        for item in items:
            if isinstance(item, BaseModel):
                rows.append(item.model_dump())
            elif isinstance(item, dict):
                rows.append(item)
            else:
                rows.append(item.__dict__)
        return pd.DataFrame(rows)

    # Custom column mapping
    rows = []
    for item in items:
        row = {}
        for col_name, extractor in columns.items():
            if callable(extractor):
                try:
                    row[col_name] = extractor(item)
                except (AttributeError, IndexError, KeyError):
                    row[col_name] = None
            else:
                # It's an attribute name
                row[col_name] = _get_nested_attr(item, extractor)
        rows.append(row)

    return pd.DataFrame(rows)


def _get_nested_attr(obj: Any, path: str) -> Any:
    """
    Get nested attribute using dot notation.

    Example: _get_nested_attr(person, "entities.0.properties.name")
    """
    try:
        for part in path.split("."):
            if part.isdigit():
                obj = obj[int(part)]
            elif isinstance(obj, dict):
                obj = obj.get(part)
            else:
                obj = getattr(obj, part, None)
            if obj is None:
                return None
        return obj
    except (AttributeError, IndexError, KeyError, TypeError):
        return None
