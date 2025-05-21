from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

Base = declarative_base()

class ProcessedEmail(Base):
    __tablename__ = 'processed_emails'
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String(256), unique=True, index=True)
    subject = Column(String(256))
    from_addr = Column(String(256))
    received_at = Column(DateTime)
    parsed_data = Column(Text)
    processed_at = Column(DateTime, default=datetime.utcnow)
