import json

from django.http import JsonResponse
from django.views import View

from library.models import Book, Author


class BooksView(View):
    @staticmethod
    def filter_books(request):
        books = Book.objects.all()

        year = request.GET.get("year")
        if year:
            books = books.filter(year=year)

        author = request.GET.get("author")
        if author:
            books = books.filter(authors__name=author)

        genre = request.GET.get("genre")
        if genre:
            books = books.filter(genre=genre)

        return books

    @staticmethod
    def get_json_book(book):
        return {
            "id": book.id,
            "title": book.title,
            "genre": book.genre,
            "authors": [author.name for author in book.authors.all()],
            "year": book.year,
        }

    @staticmethod
    def is_author(author_id):
        return Author.objects.filter(id=author_id).exists()

    def get(self, request, book_id=None):
        if book_id:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return JsonResponse({"error": "book not found"}, status=404)
            return JsonResponse(self.get_json_book(book), safe=False, status=200)

        books = self.filter_books(request)
        if not books.exists():
            return JsonResponse({"error": "books not found"}, status=404)

        json_books = [self.get_json_book(book) for book in books]
        return JsonResponse(json_books, safe=False, status=200)

    def post(self, request):
        data = json.loads(request.body)

        title = data.get("title")
        if not title:
            return JsonResponse({"error": "title is required"}, status=400)

        genre = data.get("genre")
        if not genre:
            return JsonResponse({"error": "genre is required"}, status=400)

        year = data.get("year")
        if not year:
            return JsonResponse({"error": "year is required"}, status=400)

        book = Book.objects.create(
            title=title,
            genre=genre,
            year=year,
        )

        authors = data.get("authors")
        if authors:
            for author in authors.split(","):
                if not self.is_author(author):
                    continue
                book.authors.add(author.strip())

        return JsonResponse(self.get_json_book(book), safe=False, status=200)

    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "book not found"}, status=404)

        data = json.loads(request.body)

        title = data.get("title")
        if title:
            book.title = title

        genre = data.get("genre")
        if genre:
            book.genre = genre

        year = data.get("year")
        if year:
            book.year = year

        authors = data.get("authors")
        if authors:
            book.authors.clear()
            for author in authors.split(","):
                if not self.is_author(author):
                    continue
                book.authors.add(author.strip())

        book.save()
        return JsonResponse(self.get_json_book(book), safe=False, status=200)

    @staticmethod
    def delete(request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "book not found"}, status=404)

        book.delete()

        return JsonResponse(
            {"message": f"deleted id={book_id}"}, safe=False, status=200
        )


class AuthorsView(View):
    @staticmethod
    def get_json_author(author):
        return {
            "id": author.id,
            "name": author.name,
            "books": [book.title for book in author.books.all()],
        }

    @staticmethod
    def filter_authors(request):
        authors = Author.objects.all()

        name = request.GET.get("name")
        if name:
            authors = authors.filter(name=name)

        return authors

    def get(self, request, author_id=None):
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return JsonResponse({"error": "author not found"}, status=404)
            return JsonResponse(self.get_json_author(author), safe=False, status=200)

        authors = self.filter_authors(request)
        if not authors.exists():
            return JsonResponse({"error": "authors not found"}, status=404)

        json_authors = [self.get_json_author(author) for author in authors]
        return JsonResponse(json_authors, safe=False, status=200)
