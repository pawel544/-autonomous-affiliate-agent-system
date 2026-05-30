from pydantic import BaseModel
from typing import Optional


class AffiliateProgram(BaseModel):
    name: str
    category: str
    commission_rate: Optional[str] = None
    recurring: bool = False
    cookie_duration: Optional[str] = None
    epc: Optional[float] = None
    reputation_score: int = 0
    seo_potential_score: int = 0
    competition_score: int = 0
    final_score: Optional[float] = None