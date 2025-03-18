from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase



DATABASE_URL_FEEDBACK = f"sqlite:///feedback.db"
engine = create_engine(DATABASE_URL_FEEDBACK, echo=True)

my_session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass