from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import datetime

from .models import Transaction, TransactionQuerySet


def overview(request):
    all_transaction = Transaction.objects.all()
    return render(request, 'EzyMoney/Base.html', {'user': request.user})
