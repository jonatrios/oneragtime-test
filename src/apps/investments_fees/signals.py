from datetime import date, datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver

from .models import Upfront, Membership, YearlyFees, Investor, Investment
from .utlis import yearly_fees_before, yearly_fees_after


@receiver(post_save, sender=Investment)
def post_save_investment(sender, instance, created, *args, **kwargs):
    if created:
        membership = Membership.objects.filter(investor=instance.investor).last()
        (investment_sum,) = (
            sender.objects.filter(investor=instance.investor)
            .filter(
                date_of_investment__gte=date(datetime.now().year, 1, 1),
                date_of_investment__lte=date(datetime.now().year, 12, 31),
            )
            .aggregate(Sum('investment_amount'))
            .values()
        )
        investment_sum = investment_sum if investment_sum else 0
        if instance.pay_upfront:
            Upfront.objects.create(investment=instance)
        else:
            if instance.invoice_expiring_date < settings.DATE_OF_NEW_FEE:
                amount, description = yearly_fees_before(
                    instance.investment_amount, instance.fee_percentage.fee_value
                )
                YearlyFees.objects.create(
                    investment=instance,
                    invoice_expire_date=instance.invoice_expiring_date,
                    fee_amount=amount,
                    description=description,
                )
            else:
                amount, _ = yearly_fees_after(
                    instance.investment_amount, instance.fee_percentage.fee_value
                )
                YearlyFees.objects.create(
                    investment=instance,
                    invoice_expire_date=instance.invoice_expiring_date,
                    fee_amount=amount,
                    description='After-04-2019 Fee for first year',
                )
        if investment_sum >= settings.MEMBERSHIP_MAX_AMOUNT:
            membership.membership_amount = 0
            membership.save()


@receiver(post_save, sender=Investor)
def post_save_investor_membership(sender, instance, created, *args, **kwargs):
    if created:
        Membership.objects.create(investor=instance)
