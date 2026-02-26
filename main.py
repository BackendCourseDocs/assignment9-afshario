from fastapi import FastAPI, Depends , Query
from sqlalchemy.orm import Session
from .model import  BookResponse,BookCreate
import redis
from .database import Base , engine , SessionLocal , BookDB
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_PASS=os.getenv("REDIS_PASS")
REDIS_HOST = os.getenv("localhost")

app = FastAPI()
redis_client = redis.Redis(host= REDIS_HOST, port=6379, db=0 , password=REDIS_PASS)
Base.metadata.create_all(bind=engine)

def get_db():
      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()

@app.post("/books/", response_model=BookResponse , status_code=201)
async def create_book(  book: BookCreate, db: Session = Depends(get_db)):
      db_book = BookDB(**book.model_dump())
      db.add(db_book)
      db.commit()
      if redis_client.get(book.name) is not None:
            redis_client.delete(book.name)
      return db_book


@app.get("/books/")
async def search_books(
      db: Session = Depends(get_db),
      q: str = Query(..., min_length=3, max_length=100),
      page: int = Query(1, ge=1),
      size: int = Query(10, ge=1, le=50)
):
      cached_item = redis_client.get(q)
      if cached_item is not None:
            return cached_item
      base = db.query(BookDB).filter(BookDB.name.like(f"%{q}%"))
      total = base.count()
      start = (page - 1) * size
      results = base.order_by(BookDB.id).offset(start).limit(size).all()     
      books_data = [{'id':book.id , 'name':book.name , 'author':book.author , 'year':book.year} for book in results]
      res = {
            "total": total,
            "page": page,
            "results": books_data
      }
      redis_client.set(q, res.__str__())
      return res


@app.get("/authors/search/")
async def search_authors(
      db: Session = Depends(get_db),
      author: str = Query(..., min_length=1, max_length=100),
):
      count = db.query(BookDB).filter(BookDB.author == author).count()
      return {
            "results": {"author": author, "count": count}
      }