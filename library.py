"""ตรรกะหลักของระบบยืม-คืนหนังสือ (ไม่ขึ้นกับหน้าเว็บ จึงทดสอบง่าย)"""
import json
import os
from datetime import date


class LibraryError(Exception):
    """ข้อผิดพลาดที่แสดงให้ผู้ใช้เห็นได้"""


class Library:
    def __init__(self, path=None):
        self.path = path
        self.books = []
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.books = json.load(f)

    def _save(self):
        if self.path:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=2)

    def _find(self, book_id):
        for book in self.books:
            if book["id"] == book_id:
                return book
        raise LibraryError(f"ไม่พบหนังสือรหัส {book_id}")

    def add_book(self, title, author):
        title, author = title.strip(), author.strip()
        if not title or not author:
            raise LibraryError("กรุณากรอกชื่อหนังสือและผู้แต่ง")
        new_id = max((b["id"] for b in self.books), default=0) + 1
        book = {"id": new_id, "title": title, "author": author,
                "borrower": None, "due": None}
        self.books.append(book)
        self._save()
        return book

    def borrow(self, book_id, borrower, today=None):
        book = self._find(book_id)
        borrower = borrower.strip()
        if not borrower:
            raise LibraryError("กรุณากรอกชื่อผู้ยืม")
        if book["borrower"]:
            raise LibraryError(f"“{book['title']}” ถูกยืมไปแล้ว")
        today = today or date.today()
        book["borrower"] = borrower
        book["due"] = date.fromordinal(today.toordinal() + 7).isoformat()
        self._save()
        return book

    def return_book(self, book_id):
        book = self._find(book_id)
        if not book["borrower"]:
            raise LibraryError(f"“{book['title']}” ยังไม่ได้ถูกยืม")
        book["borrower"] = None
        book["due"] = None
        self._save()
        return book

    def search(self, keyword=""):
        keyword = keyword.strip().lower()
        return [b for b in self.books
                if keyword in b["title"].lower() or keyword in b["author"].lower()]

    def overdue(self, today=None):
        today = (today or date.today()).isoformat()
        return [b for b in self.books if b["due"] and b["due"] < today]

    def stats(self):
        borrowed = sum(1 for b in self.books if b["borrower"])
        return {"total": len(self.books), "borrowed": borrowed,
                "available": len(self.books) - borrowed}
