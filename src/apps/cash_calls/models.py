from datetime import timedelta
from django.conf import settings
from django.db import models
from apps.investor.models import BaseCreateUpdateModel, Investor
from apps.investments_fees.models import Upfront, YearlyFees, Membership


# Create your models here.
class Bills(BaseCreateUpdateModel):

    choises = (
        ('G', 'generated'),
        ('V', 'validated'),
        ('S', 'sent by email'),
        ('P', 'paid'),
        ('O', 'overdue'),
    )

    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    upfront_fees = models.ManyToManyField(Upfront, blank=True)
    yearly_before = models.ManyToManyField(YearlyFees, blank=True)
    membership = models.ManyToManyField(Membership, blank=True)
    cash_call_expire = models.DateField(
        verbose_name='cash_call_expire', default=settings.CASH_CALL_EXPIRE_DATE
    )
    state = models.CharField(
        verbose_name='state', choices=choises, default='G', max_length=1
    )

    @property
    def cash_call_expire_date(self):
        return self.created_at + timedelta(days=15)

    def save(self, *args, **kwargs):
        self.cash_call_expire = self.cash_call_expire_date
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
        db_table = 'bills'
