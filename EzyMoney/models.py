from django.conf import settings
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    class TypeOperation(models.TextChoices):
        INCOME = 'IN', 'Доход'
        EXPENSE = 'EX', 'Расход'

    type_operation = models.CharField(
        max_length=2,
        choices=TypeOperation.choices,
        default=TypeOperation.EXPENSE,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money_sum = models.DecimalField(max_digits=5, decimal_places=2)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField('Category', null=True, default=None,
                                      blank=True, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', null=True, default=None,
                                blank=True, on_delete=models.CASCADE)

    def transact(self):
        self.published_date = timezone.now()
        self.save()


class Category(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Account(models.Model):
    class TypeAccount(models.TextChoices):
        CASH = 'CA', 'Наличные'
        CARD = 'CAR', 'Карта'
        BANK_ACCOUNT = 'BA', 'Банковский счёт'
        DEPOSIT = 'DE', 'Депозит'
        CREDIT = 'DE', 'Кредит'

    type_account = models.CharField(
        max_length=2,
        choices=TypeAccount.choices,
        default=TypeAccount.CASH,
    )

    currency = models.ForeignKey('Currency', null=True, default=None,
                                 blank=True, on_delete=models.CASCADE)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=type_account)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    limit = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Currency(models.TextChoices):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
