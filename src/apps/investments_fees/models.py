from django.conf import settings
from django.db import models
from apps.investor.models import BaseCreateUpdateModel, Investor, Investment


# Create your models here.
class Upfront(BaseCreateUpdateModel):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    upfront_fee_amount = models.DecimalField(verbose_name='upfront_fee_amount',max_digits=10, decimal_places=5)
    
    @property
    def calculate_upfront(self):
        return (self.investment.fee_percentage.fee_value * self.investment.investment_amount) * settings.YEARS_UPFRONT

    def save(self, *args, **kwargs):
        self.upfront_fee_amount = self.calculate_upfront
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.investment.id}: {self.upfront_fee_amount} / {self.investment.investor.first_name}'
    
    class Meta:
        verbose_name = 'Upfront fee'
        verbose_name_plural = 'Upfront fees'
        db_table = 'upfront_fees'


class Membership(BaseCreateUpdateModel):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    membership_amount = models.DecimalField(
        'membership_amount',
        blank=False,
        null=False,
        default=settings.MEMBERSHIP_YEAR_VALUE,
        max_digits=10,
        decimal_places=2,
    )
    year_of_membership = models.IntegerField(verbose_name='year_of_membership', default=1)

    def __str__(self) -> str:
        return f'{self.membership_amount} / {self.investor.first_name}'

    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        db_table = 'memberships'


class YearlyFees(BaseCreateUpdateModel):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    description = models.CharField(verbose_name='description', max_length=200, default='Fee for first year')
    fee_amount = models.DecimalField(
        'fee_amount',
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=2,
        default='0.0'
    )
    invoice_expire_date = models.DateField(
        verbose_name='invoice_expire_date',
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.investment.id}: {self.description} {self.fee_amount} / {self.investment.investor.first_name}'

    
    class Meta:
        verbose_name = 'Yearly Fee'
        verbose_name_plural = 'Yearly Fees'
        db_table = 'yearly_fees'
