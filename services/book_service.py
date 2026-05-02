from typing import List, Optional
from uuid import uuid4, UUID
from repository import book_repo
from schemas.book import BookCreate, BookResponse, BookStatus

async def fetch_books(status: Optional[BookStatus] = None, author: Optional[str] = None, sort_by: Optional[str] = None) -> List[BookResponse]:
    books_data = await book_repo.get_all_books()
    
    if status:
        books_data = [b for b in books_data if b["status"] == status.value]
    if author:
        books_data = [b for b in books_data if b["author"].lower() == author.lower()]
        
    if sort_by == "title":
        books_data.sort(key=lambda x: x["title"])
    elif sort_by == "year":
        books_data.sort(key=lambda x: x["year"])
        
    return [BookResponse(**b) for b in books_data]

async def fetch_book(book_id: UUID) -> Optional[BookResponse]:
    book = await book_repo.get_book_by_id(book_id)
    if book:
        return BookResponse(**book)
    return None

async def create_book(book: BookCreate) -> BookResponse:
    book_dict = book.model_dump()
    book_dict["id"] = uuid4()
    book_dict["status"] = book_dict["status"].value
    
    saved_book = await book_repo.add_book(book_dict)
    return BookResponse(**saved_book)

async def remove_book(book_id: UUID) -> None:
    await book_repo.delete_book(book_id)