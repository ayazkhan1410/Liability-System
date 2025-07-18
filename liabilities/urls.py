from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('bank/transaction/', views.bank_transaction, name='bank_transaction'),
    path('receivables/', views.receivables, name='receivables'),
]
