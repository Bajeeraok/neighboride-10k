from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set");
if "sslmode=" not in db_url:
    db_url = f"{db_url}{'&' if '?' in db_url else '?'}sslmode=require"
    
engine = create_engine(db_url,pool_pre_ping=True,pool_size=5,max_overflow=5,future=True)
async def verify():
    async with engine.connect() as conn:
        val await conn.scalar(text("SELECT 1"))
        print("DB OK",val)
asyncio.run(verify())


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

