from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Avg


class TransactionQuerySet(models.QuerySet):
    def all_transaction(self, **kwargs):
        return self.filter(user=kwargs['user'])

    def transaction_during_period(self, **kwargs):
        return self.filter(user=kwargs['user'], date_time__range=(kwargs['start_day'], ['end_day']))


class Transaction(models.Model):
    class TypeOperation(models.TextChoices):
        INCOME = 'IN', 'Доход'
        EXPENSE = 'EX', 'Расход'
        ADJUSTMENT = 'AD', 'Корректировка'

    type_operation = models.CharField(
        max_length=3,
        choices=TypeOperation.choices,
        default=TypeOperation.EXPENSE,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money_sum = models.DecimalField(max_digits=5, decimal_places=2)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField('Category', blank=True)
    account = models.ForeignKey('Account', null=True, default=None,
                                blank=True, on_delete=models.CASCADE)

    @classmethod
    def balance_adjustment(cls, self, **kwargs):
        global adjustment
        money_sum = cls.objects.filter(user=kwargs['user'], account=kwargs['account']).aggregate(Avg('money_sum'))

        if money_sum < kwargs['money_sum'] and kwargs['money_sum'] > 0:
            adjustment = kwargs['money_sum'] - money_sum
        elif money_sum > kwargs['money_sum'] > 0:
            adjustment = money_sum - kwargs['money_sum']

        self.money_sum = adjustment
        self.save()

    def transact(self):
        self.published_date = timezone.now()
        self.save()


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Account(models.Model):
    class TypeAccount(models.TextChoices):
        CASH = 'CA', 'Наличные'
        CARD = 'CAR', 'Карта'
        BANK_ACCOUNT = 'BA', 'Банковский счёт'
        DEPOSIT = 'DE', 'Депозит'
        CREDIT = 'CR', 'Кредит'

    type_account = models.CharField(
        max_length=3,
        choices=TypeAccount.choices,
        default=TypeAccount.CASH,
    )

    currency = models.ForeignKey('Currency', null=True, default=None,
                                 blank=True, on_delete=models.CASCADE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=type_account)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    limit = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Currency(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
