from typing import Optional
from groq import Groq
from app.models.session import Session
from app.models.user import User
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, db=None):
        self.logger = logging.getLogger(__name__)
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.db = db
        self.logger.debug("ChatService initialized")

    def _build_messages(self, session: Session, new_message: str) -> list:
        """Build the messages array for the LLM context"""
        messages = []
        
        # Add system prompt from user config
        user_config = json.loads(session.user.config)
        if 'system_prompt' in user_config:
            self.logger.debug(f"Using system prompt: {user_config['system_prompt'][:50]}...")
            messages.append({
                "role": "system",
                "content": user_config['system_prompt']
            })
        else:
            self.logger.warning("No system prompt found in user config")
        
        # Add existing transcript if it exists
        if session.transcript:
            # Split transcript into messages and convert to chat format
            transcript_messages = session.transcript.split('\n')
            for msg in transcript_messages:
                if msg.startswith('THERAPEUT*IN: '):
                    messages.append({
                        "role": "user",
                        "content": msg.replace('THERAPEUT*IN: ', '')
                    })
                elif msg.startswith('KLIENT*IN: '):
                    messages.append({
                        "role": "assistant",
                        "content": msg.replace('KLIENT*IN: ', '')
                    })
        
        # Add new message
        messages.append({
            "role": "user",
            "content": new_message
        })
        
        return messages

    def get_chat_response(self, session: Session, message: str) -> str:
        try:
            # Add therapist message to transcript first
            if session.transcript:
                session.transcript = session.transcript + f"\nTHERAPEUT*IN: {message}"
            else:
                session.transcript = f"THERAPEUT*IN: {message}"
            
            messages = self._build_messages(session, message)
            user_config = json.loads(session.user.config)
            model = settings.DEFAULT_MODEL
            
            logger.info(f"Sending request to Groq API for session {session.id}")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            assistant_message = chat_completion.choices[0].message.content
            
            # Add client response to transcript
            session.transcript = session.transcript + f"\nKLIENT*IN: {assistant_message}"
            
            # Save the updated transcript
            if self.db:
                self.db.commit()
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Failed to get chat response: {str(e)}", exc_info=True)
            raise