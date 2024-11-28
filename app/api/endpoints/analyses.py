from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.analysis import Analysis as AnalysisModel
from app.models.session import Session as SessionModel
from app.schemas.analysis import Analysis, AnalysisCreate
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/session/{session_id}", response_model=Analysis)
def create_analysis(
    session_id: str,
    analysis: AnalysisCreate,
    db: Session = Depends(get_db)
):
    """Create a new analysis for a session"""
    session = db.query(SessionModel)\
        .filter(SessionModel.id == session_id)\
        .first()
    if not session:
        logger.warning(f"Attempted to create analysis for non-existent session: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        db_analysis = AnalysisModel(**analysis.dict())
        session.analysis = db_analysis
        db.add(db_analysis)
        db.commit()
        logger.success(f"Created analysis for session {session_id}")
        return db_analysis
    except Exception as e:
        logger.error(f"Failed to create analysis for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating analysis")

@router.get("/session/{session_id}", response_model=Analysis)
def get_session_analysis(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get the analysis for a specific session"""
    analysis = db.query(AnalysisModel)\
        .join(SessionModel)\
        .filter(SessionModel.id == session_id)\
        .first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.put("/{analysis_id}", response_model=Analysis)
def update_analysis(
    analysis_id: str,
    analysis_update: AnalysisCreate,
    db: Session = Depends(get_db)
):
    """Update an existing analysis"""
    db_analysis = db.query(AnalysisModel)\
        .filter(AnalysisModel.id == analysis_id)\
        .first()
    if not db_analysis:
        logger.warning(f"Attempted to update non-existent analysis: {analysis_id}")
        raise HTTPException(status_code=404, detail="Analysis not found")

    try:
        for key, value in analysis_update.dict().items():
            setattr(db_analysis, key, value)
        db.commit()
        logger.success(f"Updated analysis {analysis_id}")
        return db_analysis
    except Exception as e:
        logger.error(f"Failed to update analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating analysis") 