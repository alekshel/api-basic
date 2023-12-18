from django.urls import path
from .views import BooksView, AuthorsView

urlpatterns = [
    path("books", BooksView.as_view()),
    path("books/<int:book_id>", BooksView.as_view()),
    path("authors", AuthorsView.as_view()),
    path("authors/<int:author_id>", AuthorsView.as_view()),
]
