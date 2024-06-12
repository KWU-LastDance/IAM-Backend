import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL
                       else {"options": "-c timezone=Asia/Seoul"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
