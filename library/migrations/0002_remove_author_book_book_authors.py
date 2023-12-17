# Generated by Django 5.0 on 2023-12-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="author",
            name="book",
        ),
        migrations.AddField(
            model_name="book",
            name="authors",
            field=models.ManyToManyField(related_name="books", to="library.author"),
        ),
    ]
