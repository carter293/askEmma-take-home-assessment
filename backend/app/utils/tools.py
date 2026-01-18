from agents import function_tool
from ..db.db import search_situation
from ..schemas import SituationSearchResult
import logging

logger = logging.getLogger(__name__)

@function_tool
async def search_policies(description: str) -> SituationSearchResult:
    """Search for the associated policy of the incident using a summary description of the situation. This will return closely related policies.

    Args:
        description: A couple sentence summary of the situation used to search.
    """
    logger.info(f"Searching policies for: {description[:100]}...")
    results = await search_situation(description=description)
    logger.info(f"Found {len(results)} matching policies")
    return results


    