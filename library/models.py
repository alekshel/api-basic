from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author", related_name="books")
    year = models.IntegerField()

    def __str__(self):
        authors = ", ".join([author.name for author in self.authors.all()])
        return f"{self.title} від {authors}, {self.year}"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
