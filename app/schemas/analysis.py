from pydantic import BaseModel
from uuid import UUID
from typing import List

class AnalysisBase(BaseModel):
    keywords: List[str]
    summary: str
    process_markers: List[str]
    recommendations: List[str]

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: UUID

    class Config:
        from_attributes = True 