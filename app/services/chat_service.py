from typing import Optional
from groq import Groq
from app.models.session import Session
from app.models.user import User
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = Groq(api_key=settings.GROQ_API_KEY)
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
            transcript = json.loads(session.transcript)
            self.logger.debug(f"Adding existing transcript with {len(transcript)} messages")
            messages.extend(transcript)
            
        # Add new message
        messages.append({
            "role": "user",
            "content": new_message
        })
        
        return messages

    async def get_chat_response(self, session: Session, message: str) -> str:
        try:
            messages = self._build_messages(session, message)
            user_config = json.loads(session.user.config)
            model = user_config.get('model', settings.DEFAULT_MODEL)
            
            logger.info(f"Sending request to Groq API for session {session.id}")
            chat_completion = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            assistant_message = chat_completion.choices[0].message.content
            session.transcript = json.dumps(messages + [{
                "role": "assistant",
                "content": assistant_message
            }])
            
            logger.success(f"Successfully generated response for session {session.id}")
            return assistant_message
            
        except Exception as e:
            logger.error(f"Failed to get chat response: {str(e)}", exc_info=True)
            raise