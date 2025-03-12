from src.database import Base
from sqlalchemy import Column, String, Integer


class FeedbackORM(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    message = Column(String)
