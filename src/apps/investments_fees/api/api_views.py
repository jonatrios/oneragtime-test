from datetime import date
from django.db.models import Sum
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..models import YearlyFees
from .serializers import UpfrontSerializer, MembershipSerializer, YearlyFeesSerializer
from apps.investor.api.serializers import InvestorSerializer, InvestmentSerializer
from ..utlis import yearly_fees_after, yearly_fees_before

# Views to list or update the diffetent kind of fees
# D.R.Y.: Tried to inherit to reuse the funcionalites of a view
investor = openapi.Parameter('investor', openapi.IN_QUERY, description="investor ID", type=openapi.TYPE_STRING)

class UpFrontApiView(views.APIView):
    '''
    List all Upfront fees or could be filter given an investor
    '''

    filter_dict = None
    serializer_class = UpfrontSerializer

    
    def get_queryset(self, investor):
        queryset = (
            self.serializer_class.Meta.model.objects.filter(**self.filter_dict)
            if self.filter_dict
            else self.serializer_class.Meta.model.objects.all()
        )
        return (
            queryset.filter(
                investment__investor=investor,
            )
            if investor
            else queryset
        )
    
    @swagger_auto_schema(manual_parameters=[investor],tags=['lists fees'])
    def get(self, request, *args, **kwargs):
        investor = request.query_params.get('investor')
        try:
            queryset = self.get_queryset(investor)
            if queryset:
                serialized_data = self.serializer_class(queryset, many=True)
                return Response(serialized_data.data)
            return Response(
                {'error': f'No investor with id {investor}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {'error': 'Investor ID must be type int'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MembershipAPIView(UpFrontApiView):
    '''
    List all Membership fees or could be filter given an investor
    '''

    serializer_class = MembershipSerializer

    def get_queryset(self, investor):
        queryset = (
            self.serializer_class.Meta.model.objects.filter(**self.filter_dict)
            if self.filter_dict
            else self.serializer_class.Meta.model.objects.all()
        )
        return (
            queryset.filter(
                investor=investor,
            )
            if investor
            else queryset
        )


class YearlyFeesBeforeAPIView(UpFrontApiView):
    '''
    List all Yearly Fees Before 04-2019 or could be filter given an investor
    '''

    filter_dict = {'description__icontains': 'before'}
    serializer_class = YearlyFeesSerializer


class YearlyFeesAfterAPIView(YearlyFeesBeforeAPIView):
    '''
    List all Yearly Fees After 04-2019 or could be filter given an investor
    '''

    filter_dict = {'description__icontains': 'after'}


class UpdateMembership(views.APIView):
    '''
    Update the Membership fees based on the creation date of an investor\n
    if the investor is active and more than a year, it generates the fees needed
    '''

    serializer_class = MembershipSerializer

    def get_queryset(self, investor):
        print((date.today() - investor.created_at).days if investor else 0)

    @swagger_auto_schema(manual_parameters=[investor],tags=['update fees'])
    def get(self, request, *args, **kwargs):
        investor = request.query_params.get('investor')
        investor_instance = InvestorSerializer.Meta.model.objects.filter(
            id=int(investor)
        ).first()
        creation_year = investor_instance.created_at.year
        years = (
            ((date.today() - investor_instance.created_at).days // 365)
            if investor
            else 0
        )
        new_membership = []
        if years and years >= 2:
            for i in range(1, years + 1):
                obj, create = MembershipSerializer.Meta.model.objects.get_or_create(
                    investor=investor_instance, year_of_membership=i
                )
                (investment_sum,) = (
                    InvestmentSerializer.Meta.model.objects.filter(
                        investor=obj.investor
                    )
                    .filter(
                        date_of_investment__gte=date(creation_year, 1, 1),
                        date_of_investment__lte=date(creation_year, 12, 31),
                    )
                    .aggregate(Sum('investment_amount'))
                    .values()
                )
                if investment_sum:
                    if investment_sum >= settings.MEMBERSHIP_MAX_AMOUNT:
                        obj.membership_amount = 0
                        obj.save()
                if create:
                    new_membership.append(MembershipSerializer(instance=obj).data)
                creation_year += 1
            if new_membership:
                return Response({'investor': int(investor), 'new_fees': new_membership})
        return Response([], status=status.HTTP_204_NO_CONTENT)


class UpdateYearlyFeesBefore(views.APIView):
    '''
    For dates before 04-2019:\n
    Generate new Yearly (if needed) fees based on the date of the investment applying the
    business rules, or update the description if is already generated
    '''

    date_filter = {'date_of_investment__lt': settings.DATE_OF_NEW_FEE}

    def get_queryset(self, investor):
        queryset = (
            InvestmentSerializer.Meta.model.objects.filter(investor=investor)
            .filter(**self.date_filter)
            .filter(pay_upfront=False)
        )
        return queryset

    def yearly_handler(self, *args, **kwargs):
        return yearly_fees_before(*args, **kwargs)

    @swagger_auto_schema(manual_parameters=[investor],tags=['update fees'])
    def get(self, request, *args, **kwargs):
        investor = request.query_params.get('investor')
        is_active = InvestorSerializer.Meta.model.objects.get(id=investor).is_active
        if is_active:
            investments = self.get_queryset(investor)
            new_fees = []
            for ele in investments:
                if ele.in_years >= 2:
                    for i in range(2, ele.in_years + 1):
                        current = ele.date_of_investment
                        fee_amount, description = self.yearly_handler(
                            ele.investment_amount, ele.fee_percentage.fee_value, year=i
                        )
                        data_dict = dict(
                            investment=ele,
                            invoice_expire_date=date(
                                current.year + i, current.month, current.day
                            ),
                            fee_amount=fee_amount,
                        )
                        try:
                            obj, create = YearlyFees.objects.get_or_create(**data_dict)
                            if obj.description != description:
                                obj.description = description
                                obj.save()
                            if create:
                                new_fees.append(YearlyFeesSerializer(instance=obj).data)
                        except YearlyFees.MultipleObjectsReturned:
                            query_filter = YearlyFees.objects.filter(**data_dict)
                            for obj in query_filter:
                                if obj.description != description:
                                    obj.description = description
                                    obj.save()
                            continue
            if new_fees:
                return Response({'investor': int(investor), 'new_fees': new_fees})
            else:
                return Response([], status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'investor is inactive'}, status=status.HTTP_404_NOT_FOUND
        )


class UpdateYearlyFeesAfter(UpdateYearlyFeesBefore):
    '''
    Same as Yearle Fees Before, but in this case for fees AFTER 04-2019
    '''

    date_filter = {'date_of_investment__gte': settings.DATE_OF_NEW_FEE}

    def yearly_handler(self, *args, **kwargs):
        return yearly_fees_after(*args, **kwargs)
