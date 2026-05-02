from typing import List, Dict, Optional
from uuid import UUID
from models import db

async def get_all_books() -> List[Dict]:
    return db

async def get_book_by_id(book_id: UUID) -> Optional[Dict]:
    for book in db:
        if book["id"] == book_id:
            return book
    return None

async def add_book(book_data: Dict) -> Dict:
    db.append(book_data)
    return book_data

async def delete_book(book_id: UUID) -> bool:
    global db
    initial_length = len(db)
    db[:] = [book for book in db if book["id"] != book_id]
    return len(db) < initial_length