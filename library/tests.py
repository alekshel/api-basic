import pytest
from django.test import Client
from .models import Book, Author


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_get_book(client):
    author = Author.objects.create(name="Сергій Джус")

    book = Book.objects.create(
        title="Laborum dolore sapiente.",
        genre="Комедія",
        year=1998,
    )
    book.authors.add(author)

    response = client.get(f"/books/{book.id}")
    assert response.status_code == 200
    assert book.id == response.json()["id"]

    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = client.get("/books?genre=Комедія")
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = client.get(f"/books/99999999999")
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_book(client):
    author = Author.objects.create(name="Сергій Джус")

    response = client.post(
        "/books",
        {
            "title": "Laborum dolore sapiente.",
            "genre": "Комедія",
            "year": 1998,
            "authors": str(author.id),
        },
        content_type="application/json",
    )
    assert response.status_code == 200

    response = client.post(
        "/books",
        {
            "title": "Laborum dolore sapiente.",
        },
        content_type="application/json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_book(client):
    author = Author.objects.create(name="Сергій Джус")

    book = Book.objects.create(
        title="Laborum dolore sapiente.",
        genre="Комедія",
        year=1998,
    )
    book.authors.add(author)

    response = client.put(
        f"/books/{book.id}",
        {
            "genre": "Жахи",
        },
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["genre"] == "Жахи"

    response = client.put(
        f"/books/99999999999",
        {
            "genre": "Жахи",
        },
        content_type="application/json",
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_book(client):
    author = Author.objects.create(name="Сергій Джус")

    book = Book.objects.create(
        title="Laborum dolore sapiente.",
        genre="Комедія",
        year=1998,
    )
    book.authors.add(author)

    response = client.delete(f"/books/{book.id}")
    assert response.status_code == 200

    response = client.get(f"/books/{book.id}")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_author(client):
    author = Author.objects.create(name="Сергій Джус")

    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 200
    assert author.id == response.json()["id"]

    response = client.get("/authors")
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = client.get("/authors?name=Сергій Джус")
    assert response.status_code == 200
    assert len(response.json()) > 0

    response = client.get(f"/authors/99999999999")
    assert response.status_code == 404
