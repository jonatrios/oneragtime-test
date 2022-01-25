from rest_framework import serializers
from ..models import Upfront, YearlyFees, Membership, Bills
from apps.investments_fees.api.serializers import (
    UpfrontSerializer,
    MembershipSerializer,
    YearlyFeesSerializer,
)


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        return {
            'id_bill': instance.id,
            'investor': instance.investor.first_name,
            'upfront_fees': UpfrontSerializer(
                Upfront.objects.filter(investment__investor=instance.investor),
                many=True,
            ).data,
            'yearly_before': YearlyFeesSerializer(
                YearlyFees.objects.filter(investment__investor=instance.investor),
                many=True,
            ).data,
            'membership': MembershipSerializer(
                Membership.objects.filter(investor=instance.investor), many=True
            ).data,
            'cash_call_expire': instance.cash_call_expire,
            'state': instance.state,
        }
