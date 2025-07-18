from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def bank_transaction(request):
    return render(request, 'bank-transaction.html')


def receivables(request):
    return render(request, 'receivables.html')
