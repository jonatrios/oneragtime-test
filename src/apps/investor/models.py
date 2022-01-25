from datetime import date, datetime
from django.db import models
from django.conf import settings


# Create your models here.
class BaseCreateUpdateModel(models.Model):
    created_at = models.DateField(verbose_name='created_at', default=date.today)
    updated_at = models.DateField(verbose_name='updated_at', auto_now=True)

    class Meta:
        abstract = True


class Investor(BaseCreateUpdateModel):
    first_name = models.CharField(
        verbose_name='inversor_name', max_length=255, null=False, blank=False
    )
    last_name = models.CharField(
        verbose_name='inversor_last_name', max_length=255, null=False, blank=False
    )
    company_name = models.CharField(
        verbose_name='company_name',
        max_length=255,
        null=True,
        blank=True,
        default='No company',
    )
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    email = models.EmailField(verbose_name='email', unique=True, null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} / {self.company_name}'

    class Meta:
        verbose_name = 'Investor'
        verbose_name_plural = 'Investors'
        db_table = 'investors'


class FeePercentage(BaseCreateUpdateModel):
    description = models.CharField(
        verbose_name='fee_description',
        max_length=200,
        blank=False,
        null=False,
        default='Some fee',
    )
    fee_value = models.DecimalField(
        'fee_value',
        blank=False,
        null=False,
        default=settings.FEE_VALUE_DEFAULT,
        max_digits=10,
        decimal_places=5,
    )

    def __str__(self) -> str:
        return f'{self.description} : {self.fee_value}'

    class Meta:
        verbose_name = 'Fee Percentage'
        verbose_name_plural = 'Fees Percentages'
        db_table = 'fees'


class Investment(models.Model):
    investment_amount = models.DecimalField(
        verbose_name='investment_amount', max_digits=10, decimal_places=2
    )
    date_of_investment = models.DateField(
        verbose_name='date_of_investment', default=datetime.today
    )
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    pay_upfront = models.BooleanField(verbose_name='pay_upfront', default=False)
    fee_percentage = models.ForeignKey(
        FeePercentage, on_delete=models.CASCADE, default=settings.FEE_VALUE_DEFAULT
    )

    @property
    def days_elapsed(self):
        return (date.today() - self.date_of_investment).days

    @property
    def in_years(self):
        return self.days_elapsed // 365

    @property
    def invoice_expiring_date(self):
        current = self.date_of_investment
        return date(current.year + 1, current.month, current.day)

    def __str__(self) -> str:
        return f'{self.investor.first_name}: ${self.investment_amount}'

    class Meta:
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'
        db_table = 'investments'
