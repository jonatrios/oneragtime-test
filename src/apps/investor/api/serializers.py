from django.conf import settings
from rest_framework import serializers
from ..models import Investment, Investor, FeePercentage


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ('id', 'first_name', 'last_name', 'company_name', 'email', 'is_active')


class FeePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePercentage
        fields = ('id', 'description', 'fee_value')


class InvestmentSerializer(serializers.ModelSerializer):
    date_of_investment = serializers.DateField(
        input_formats=settings.DATE_INPUT_FORMATS
    )

    class Meta:
        model = Investment
        fields = (
            'id',
            'investment_amount',
            'date_of_investment',
            'investor',
            'fee_percentage',
            'pay_upfront',
        )

    def to_representation(self, instance):
        fee_percentage = (
            FeePercentageSerializer(instance=instance.fee_percentage).data['fee_value']
            if FeePercentageSerializer(instance=instance.fee_percentage).data[
                'description'
            ]
            else '0.0'
        )
        return {
            'id': instance.id,
            'investment_amount': instance.investment_amount,
            'date_of_investment': instance.date_of_investment,
            'investor': instance.investor.__str__(),
            'fee_percentage': fee_percentage,
            'days_elapsed': instance.days_elapsed,
            'in_years': instance.in_years,
            'pay_upfront': instance.pay_upfront,
        }
