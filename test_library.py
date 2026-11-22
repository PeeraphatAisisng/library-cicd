from datetime import date

import pytest

from library import Library, LibraryError


@pytest.fixture
def lib():
    library = Library()
    library.add_book("Clean Code", "Robert C. Martin")
    library.add_book("DevOps Handbook", "Gene Kim")
    return library


def test_add_book_gives_running_id(lib):
    book = lib.add_book("Python", "Guido")
    assert book["id"] == 3
    assert lib.stats() == {"total": 3, "borrowed": 0, "available": 3}


def test_add_book_requires_title_and_author(lib):
    with pytest.raises(LibraryError):
        lib.add_book("  ", "someone")


def test_borrow_sets_due_date_7_days(lib):
    book = lib.borrow(1, "Somchai", today=date(2026, 11, 1))
    assert book["borrower"] == "Somchai"
    assert book["due"] == "2026-11-08"


def test_cannot_borrow_twice(lib):
    lib.borrow(1, "A")
    with pytest.raises(LibraryError):
        lib.borrow(1, "B")


def test_return_book(lib):
    lib.borrow(2, "A")
    lib.return_book(2)
    assert lib.stats()["borrowed"] == 0


def test_cannot_return_available_book(lib):
    with pytest.raises(LibraryError):
        lib.return_book(1)


def test_unknown_book(lib):
    with pytest.raises(LibraryError):
        lib.borrow(99, "A")


def test_search_by_title_or_author(lib):
    assert [b["id"] for b in lib.search("clean")] == [1]
    assert [b["id"] for b in lib.search("kim")] == [2]


def test_overdue(lib):
    lib.borrow(1, "A", today=date(2026, 11, 1))
    assert lib.overdue(today=date(2026, 11, 9))[0]["id"] == 1
    assert lib.overdue(today=date(2026, 11, 8)) == []


def test_data_is_saved_to_file(tmp_path):
    path = tmp_path / "books.json"
    Library(str(path)).add_book("Saved", "Writer")
    assert Library(str(path)).books[0]["title"] == "Saved"
