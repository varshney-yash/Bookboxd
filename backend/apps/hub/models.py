from django.db import models
from django.contrib.auth.models import User

class BookList(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ListBook(models.Model):
    book_list = models.ForeignKey(BookList, on_delete=models.CASCADE)
    google_books_id = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book_list', 'google_books_id')

    def __str__(self):
        return f"{self.book_list.name} - {self.google_books_id}"