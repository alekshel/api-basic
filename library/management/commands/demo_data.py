import random

from django.core.management.base import BaseCommand
from faker import Faker

from library.models import Book, Author

fake = Faker("uk")

GENRES = ["Драма", "Комедія", "Фантастика", "Жахи", "Пригоди", "Фентезі"]


class Command(BaseCommand):
    help = "Demo books data"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        Author.objects.all().delete()

        for _ in range(50):
            Author.objects.create(name=fake.name())

        for _ in range(100):
            book = Book.objects.create(
                title=fake.sentence(),
                genre=random.choice(GENRES),
                year=random.randint(1980, 2023),
            )

            for _ in range(random.randint(1, 3)):
                author = random.randint(1, 50)
                book.authors.add(author)

        self.stdout.write(self.style.SUCCESS("Successfully added"))
