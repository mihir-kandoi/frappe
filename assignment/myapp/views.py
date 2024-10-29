from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
import requests

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [filters.SearchFilter] # to filter books by title and authors
    search_fields = ['title', 'authors']

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'outstanding' : ['gte', 'lte']}

class TransactionViewSet(viewsets.ModelViewSet):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

def find_transactions(request):
    member = request.GET.get('member')
    book = request.GET.get('book')
    transactions = Transaction.objects.filter(issued_on__isnull = False, returned_on__isnull = True)
    if not transactions:
        return JsonResponse({"error": "No pending transactions or no book has been issued yet"}, status = status.HTTP_400_BAD_REQUEST)
    if not member and not book:
        return JsonResponse({'members': list(transactions.values_list('member', flat=True).distinct())})
    elif member and not book:
        return JsonResponse({'books': list(transactions.filter(member=member).values_list('book', flat=True).distinct())})
    elif member and book:
        return JsonResponse({'transactions': list(transactions.filter(member=member, book=book).values_list('id', flat=True))})
        
@csrf_exempt
def return_transaction(request, id):
    try:
        transaction = Transaction.objects.get(id=id)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
    if transaction.returned_on:
        return JsonResponse({'error': 'This book has already been returned.'}, status=status.HTTP_400_BAD_REQUEST)
    if transaction.penalty_date < timezone.datetime.now().date():
        transaction.member.outstanding += 750
        transaction.penalty_applied = True
    elif transaction.penalty_date >= timezone.datetime.now().date():
        transaction.member.outstanding += 500
    transaction.returned_on = timezone.datetime.now().date()
    transaction.book.qty_in_stock += 1
    transaction.book.save()
    transaction.member.save()
    transaction.save()
    if transaction.penalty_applied == True:
        return JsonResponse({'message': "success", "penalty_applied": True})
    else:
    	return JsonResponse({'message': "success", "penalty_applied": False})
    
def get_books(request_data, qty, data=[], page=1):
    request_data["page"] = page
    response = requests.get(url="https://frappe.io/api/method/frappe-library", params=request_data).json()['message']

    if not response: # return if response is empty ie there are no more books with the given paramaters
        return data
    
    unique_data = {} # this block will remove duplicate books received in the response
    for sub_data in response:
        sub_data_id = sub_data['bookID']
        if sub_data_id not in unique_data:
            unique_data[sub_data_id] = sub_data
    response = list(unique_data.values())

    response = [item for item in response if item not in data] # this will remove duplicates from this reponse by checking the responses of previous pages
    response = [item for item in response if Book.objects.filter(pk=item['bookID']).exists() == False] # this will remove duplicates from the books already in the database
    data.extend(response) # append the sanitized response to the dataset
    if qty:
        if qty == len(response): # we have got the required amount of books, return.
            return data
        elif qty < len(response): # this response has more number of books than we require so we anyway add it to our dataset then remove the extra books not needed
            diff = len(response) - qty
            del data[-diff:]
            return data
        else: # call this function again to request more books from Frappe server
            return get_books(request_data=request_data, qty=qty - len(response), data=data, page=page+1)
    else: # if qty not specified then return the sanitized data
        return response

@api_view(['POST'])
def import_books(request):
    qty = request.data.pop('qty', None)
    response = get_books(request.data, qty, data=[])
    try:
        for object in response:
            object['num_pages'] = object.pop('  num_pages')
        serializer = BooksSerializer(data=response, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"books_added": len(response)}, status=201)
        else:
            return HttpResponse(serializer.errors, status=500)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
