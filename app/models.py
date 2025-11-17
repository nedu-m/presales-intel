from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class Brief(Base):
    """Database model for generated briefs"""
    __tablename__ = "briefs"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    meeting_date = Column(DateTime, nullable=True)
    attendees = Column(Text, nullable=True)
    
    # Generated content
    company_context = Column(Text)
    attendee_analysis = Column(Text, nullable=True)
    tech_stack = Column(Text, nullable=True)
    competitive_landscape = Column(Text, nullable=True)
    suggested_questions = Column(Text, nullable=True)
    full_brief = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

