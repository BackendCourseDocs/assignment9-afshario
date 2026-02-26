from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100  ),
    author: str = Field(...),
    year: int = Field(...),

class BookResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=100  ),
    author: str = Field(...),
    year: int = Field(...),