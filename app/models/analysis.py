from sqlalchemy import Column, String, Text
from app.db.session import Base
import uuid
import json

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    _keywords = Column('keywords', Text, default='[]')
    summary = Column(Text)
    _process_markers = Column('process_markers', Text, default='[]')
    _recommendations = Column('recommendations', Text, default='[]')

    @property
    def keywords(self):
        return json.loads(self._keywords)

    @keywords.setter
    def keywords(self, value):
        self._keywords = json.dumps(value)

    @property
    def process_markers(self):
        return json.loads(self._process_markers)

    @process_markers.setter
    def process_markers(self, value):
        self._process_markers = json.dumps(value)

    @property
    def recommendations(self):
        return json.loads(self._recommendations)

    @recommendations.setter
    def recommendations(self, value):
        self._recommendations = json.dumps(value) 