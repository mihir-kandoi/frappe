from rest_framework import serializers
from .models import Book, Member, Transaction

class BooksSerializer(serializers.ModelSerializer):
	publication_date = serializers.DateField(format='%m/%d/%Y', input_formats=['%m/%d/%Y'])
	class Meta:
		model = Book
		fields = ['bookID', 'title', 'authors', 'average_rating', 'isbn', 'isbn13', 'language_code', 'num_pages', 'ratings_count', 'text_reviews_count', 'publication_date', 'publisher', 'qty_in_stock']

class MemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = Member
		fields = ['id', 'name', 'number', 'email', 'outstanding']

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ['id', 'book', 'member', 'issued_on', 'returned_on', 'penalty_date', "penalty_applied"]