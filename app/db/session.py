import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.models.products import Products

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
    session = SessionLocal()
    apple1 = Products(name="사과 - 특상", description="사과 - 특상", category="과일", stock=100)
    apple2 = Products(name="사과 - 상", description="사과 - 상", category="과일", stock=100)
    apple3 = Products(name="사과 - 중", description="사과 - 중", category="과일", stock=100)
    session.add_all([apple1, apple2, apple3])
    session.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
