from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, List
from app.db.session import get_db
from app.services.analysis_service import AnalysisService
import logging
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)

class AnalysisResponse(BaseModel):
    id: str
    summary: str
    keywords: List[str]
    process_markers: List[str]
    recommendations: List[str]

@router.post("/{session_id}", response_model=AnalysisResponse)
async def analyze_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Analyze a therapy session and return summary, keywords, process markers, and recommendations
    """
    logger.info(f"Starting analysis for session {session_id}")
    
    try:
        analysis_service = AnalysisService(db)
        analysis = await analysis_service.create_analysis(session_id)
        
        logger.info(f"Analysis completed for session {session_id}")
        return AnalysisResponse(
            id=analysis.id,
            summary=analysis.summary,
            keywords=analysis.keywords,
            process_markers=analysis.process_markers,
            recommendations=analysis.recommendations
        )
    except ValueError as e:
        logger.warning(f"Attempted to analyze non-existent session: {session_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing session") 