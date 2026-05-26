from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    company_size = Column(Integer)
    industry = Column(String)
    email_opens = Column(Integer)
    website_visits = Column(Integer)
    demo_requested = Column(Integer)
    lead_source = Column(String)

    probability = Column(Float)
    score = Column(Integer)
    category = Column(String)