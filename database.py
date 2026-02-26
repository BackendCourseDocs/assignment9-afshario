from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
SERVER = os.getenv("DB_SERVER")
PORT = os.getenv("DB_PORT")
DB = os.getenv("DB")

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASS}@{SERVER}:{PORT}/{DB}",
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    author = Column(String(100))
    year = Column(Integer)