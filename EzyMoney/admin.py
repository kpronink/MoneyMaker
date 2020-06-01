from django.contrib import admin
from .models import Transaction
from .models import Category
from .models import Account
from .models import Plans
from .models import Goals
from .models import Currency

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Plans)
admin.site.register(Goals)
admin.site.register(Currency)
# Register your models here.
