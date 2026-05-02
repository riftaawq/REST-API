from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from schemas.book import BookCreate, BookResponse, BookStatus
from services import book_service

router = APIRouter()

@router.get("/books", response_model=List[BookResponse])
async def get_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="sort by 'title' or 'year'")
):
    return await book_service.fetch_books(status, author, sort_by)

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID):
    book = await book_service.fetch_book(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
    return book

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await book_service.remove_book(book_id)