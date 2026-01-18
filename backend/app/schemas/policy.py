from pydantic import BaseModel


class SituationSearchResult(BaseModel):
    id: int
    distance: float
    full_policy_text: str
    situation_description: str