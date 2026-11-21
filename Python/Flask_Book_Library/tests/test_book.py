import pytest
from project.books.models import Book


# 1. Testy poprawnych danych
def test_valid_book():
    b = Book(name="Wiedzmin", author="Sapkowski", year_published=1993, book_type="fantasy")
    assert b.name == "Wiedzmin"
    assert b.author == "Sapkowski"
    assert b.year_published == 1993
    assert b.book_type == "fantasy"
    assert b.status == "available"   


def test_valid_custom_status():
    b = Book(name="Lalka", author="Prus", year_published=1890, book_type="novel", status="borrowed")
    assert b.status == "borrowed"


# 2. Testy niepoprawnych danych
def test_year_as_text_should_fail():
    b = Book(name="X", author="Y", year_published="to nie rok", book_type="novel")
    assert isinstance(b.year_published, int), "Rok powinien byc liczba calkowita"


def test_negative_year_should_fail():
    b = Book(name="X", author="Y", year_published=-500, book_type="novel")
    assert b.year_published > 0, "Rok wydania nie moze byc ujemny"


def test_empty_name_should_fail():
    b = Book(name="", author="Y", year_published=2000, book_type="novel")
    assert b.name != "", "Nazwa ksiazki nie moze byc pusta"


# 3. Testy wstrzykniecia SQL i JavaScript
def test_sql_injection_in_name():
    payload = "'; DROP TABLE books; --"
    b = Book(name=payload, author="Y", year_published=2000, book_type="novel")
    assert "DROP TABLE" not in b.name, "Wykryto potencjalny SQL injection w polu name"


def test_js_injection_in_author():
    payload = "<script>alert('xss')</script>"
    b = Book(name="X", author=payload, year_published=2000, book_type="novel")
    assert "<script>" not in b.author, "Wykryto potencjalny XSS/JS injection w polu author"


# 4. Testy EKSTREMALNE
def test_very_long_name():
    long_name = "A" * 10000
    b = Book(name=long_name, author="Y", year_published=2000, book_type="novel")
    assert len(b.name) <= 64, "Nazwa przekracza dozwolona dlugosc 64 znakow"


def test_extreme_year():
    b = Book(name="X", author="Y", year_published=999999999, book_type="novel")
    assert 0 < b.year_published <= 2100, "Rok poza rozsadnym zakresem"