from django.contrib import admin
from .models import Transaction
from .models import Category

admin.site.register(Transaction)
admin.site.register(Category)
# Register your models here.
