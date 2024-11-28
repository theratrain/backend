from datetime import datetime
import uuid
import json
import logging
from groq import Groq
from app.models.analysis import Analysis
from app.models.session import Session
from app.core.config import settings

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, db=None):
        self.logger = logging.getLogger(__name__)
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.db = db
        self.logger.debug("AnalysisService initialized")

    def _build_messages(self, transcript: str) -> list:
        """Build the messages array for the LLM context"""
        return [{
            "role": "user",
            "content": f"""Analyze the following therapy session transcript and provide:

            1. A concise summary of the session
            2. Key therapeutic keywords (max 5)
            3. Process markers - important moments or shifts in the session (2-4 items)
            4. Recommendations for the next session (2-3 items)

            Transcript:
            {transcript}

            Provide the response in JSON format with these keys:
            - summary (string)
            - keywords (array of strings)
            - process_markers (array of strings)
            - recommendations (array of strings)
            """
        }]

    async def create_analysis(self, session_id: str) -> Analysis:
        """Create an analysis for a therapy session"""
        try:
            # Get the session
            session = self.db.query(Session).filter(Session.id == session_id).first()
            if not session:
                self.logger.warning(f"Session not found: {session_id}")
                raise ValueError("Session not found")

            # Build messages and send to model
            messages = self._build_messages(session.transcript)
            
            self.logger.info(f"Sending analysis request to Groq API for session {session_id}")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=settings.DEFAULT_MODEL,
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=1024,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_text = chat_completion.choices[0].message.content
            analysis_data = json.loads(analysis_text)
            self.logger.debug(f"Received analysis response for session {session_id}")

            # Create analysis record
            analysis = Analysis(
                id=str(uuid.uuid4()),
                keywords=analysis_data["keywords"] if "keywords" in analysis_data else [],
                process_markers=analysis_data["process_markers"] if "process_markers" in analysis_data else [],
                recommendations=analysis_data["recommendations"] if "recommendations" in analysis_data else [],
                summary=analysis_data["summary"]
            )

            self.db.add(analysis)
            self.db.commit()
            
            self.logger.info(f"Analysis created for session {session_id}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to create analysis: {str(e)}", exc_info=True)
            if self.db:
                self.db.rollback()
            raise
