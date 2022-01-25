from rest_framework import serializers
from ..models import Upfront, Membership, YearlyFees


class UpfrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upfront
        fields = ('id', 'investment', 'upfront_fee_amount')

    def to_representation(self, instance):
        return {
            'investment_id': instance.investment.id,
            'investment_amount': instance.investment.investment_amount,
            'upfront_fee': instance.upfront_fee_amount,
            'invoice_expiring_date': instance.investment.invoice_expiring_date,
        }


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'membership_amount')

    def to_representation(self, instance):
        return {
            'membership_amount': instance.membership_amount,
            'year_of_membership': instance.year_of_membership,
        }


class YearlyFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyFees
        fields = (
            'id',
            'investment',
            'description',
            'fee_amount',
            'invoice_expire_date',
        )

    def to_representation(self, instance):
        return {
            'investment_id': instance.investment.id,
            'investment_amount': instance.investment.investment_amount,
            'fee_amount': instance.fee_amount,
            'description': instance.description,
            'invoice_expiring_date': instance.invoice_expire_date,
        }
