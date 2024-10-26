from django.urls import include, path
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()

router.register(r'books', BooksViewSet)
router.register(r'members', MemberViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls')),
    path('transactions/<int:id>/return/', views.return_transaction, name='return_transaction'),
    path('import-books/', views.import_books, name='import_books')
]
