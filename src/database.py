from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = f"sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

my_session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass