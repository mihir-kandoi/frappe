from django.db import models

class Book(models.Model):
    bookID = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    isbn = models.CharField(max_length=20)
    isbn13 = models.CharField(max_length=20)
    language_code = models.CharField(max_length=10)
    num_pages = models.PositiveIntegerField()
    ratings_count = models.PositiveIntegerField()
    text_reviews_count = models.PositiveIntegerField()
    publication_date = models.DateField()
    publisher = models.CharField(max_length=255)
    qty_in_stock = models.PositiveIntegerField(default=5)
    
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    outstanding = models.PositiveIntegerField(
        default=0
    )

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    issued_on = models.DateField(null=True, blank=True)
    returned_on = models.DateField(null=True, blank=True)
    penalty_date = models.DateField(null=True, blank=True)
    penalty_applied = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.returned_on:
            if self.member.outstanding > 500:
                raise ValidationError("Cannot issue book: Member's outstanding balance exceeds 500.", code=400)
            self.issued_on = timezone.now().date()
            self.penalty_date = self.issued_on + timedelta(days=1)
            self.book.qty_in_stock -= 1
            self.book.save()
        super().save(*args, **kwargs)