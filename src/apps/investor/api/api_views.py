from rest_framework import viewsets
from .serializers import InvestorSerializer, InvestmentSerializer, FeePercentageSerializer


class InvestorModelViewSet(viewsets.ModelViewSet):
    '''
    Model viewset for CRUD Investors
    '''

    serializer_class = InvestorSerializer
    queryset = InvestorSerializer.Meta.model.objects.all()


class FeePercentageModelViewSet(viewsets.ModelViewSet):
    '''
    Model viewset for CRUD Fees Percentages
    '''

    serializer_class = FeePercentageSerializer
    queryset = FeePercentageSerializer.Meta.model.objects.all()

class InvestmentModelViewSet(viewsets.ModelViewSet):
    '''
    Model viewset for CRUD Investments
    '''

    serializer_class = InvestmentSerializer

    def get_queryset(self):
        queryset = InvestmentSerializer.Meta.model.objects.all()
        investor = self.request.query_params.get('investor')
        if investor:
            queryset = queryset.filter(investor=investor)
        return queryset
