from fastapi import FastAPI, Depends , Query
from sqlalchemy.orm import Session
from .model import  BookResponse,BookCreate
from .database import Base , engine , SessionLocal , BookDB

app = FastAPI()
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
      return db_book


@app.get("/books/")
async def search_books(
      db: Session = Depends(get_db),
      q: str = Query(..., min_length=3, max_length=100),
      page: int = Query(1, ge=1),
      size: int = Query(10, ge=1, le=50)
):

      base = db.query(BookDB).filter(BookDB.name.like(f"%{q}%"))
      total = base.count()
      start = (page - 1) * size
      results = base.order_by(BookDB.id).offset(start).limit(size).all()     
      return {
            "total": total,
            "page": page,
            "results": results
      }


@app.get("/authors/search/")
async def search_authors(
      db: Session = Depends(get_db),
      author: str = Query(..., min_length=1, max_length=100),
):
      count = db.query(BookDB).filter(BookDB.author == author).count()
      return {
            "results": {"author": author, "count": count}
      }