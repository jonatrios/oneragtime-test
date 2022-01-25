from datetime import date
from random import choice
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import BillsSerializer

bill_id = openapi.Parameter('bill', openapi.IN_QUERY, description="bill ID", type=openapi.TYPE_STRING)

# Generete New Bills (Cash Calls) based on the fees avaiables 
class BillsGenericViewSet(viewsets.GenericViewSet):
    serializer_class = BillsSerializer

    def get_queryset(self):
        queryset = BillsSerializer.Meta.model.objects.all()
        state = self.request.query_params.get('state')
        if state:
            queryset = queryset.filter(state=state)
        return queryset

    def list(self, request, *args, **kwargs):
        investor = self.request.query_params.get('investor')
        serialized_data = self.get_serializer(self.get_queryset().filter(investor=investor), many=True)
        return Response(serialized_data.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serilized_data = self.get_serializer(instance=instance)
        return Response(serilized_data.data)

    def create(self, request, *args, **kwargs):
        to_serlializer = self.get_serializer(data=request.data)
        if to_serlializer.is_valid():
            to_serlializer.save()
            return Response(to_serlializer.data)
        return Response(to_serlializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        to_serlializer = self.get_serializer(instance, data=request.data, partial=partial)
        if to_serlializer.is_valid():
            to_serlializer.save()
            return Response(to_serlializer.data)
        return Response(to_serlializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def parcial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# This API Views Simulate the proccess to check for the diffent states of one bill based on certain investor
class SimulateVerificationAPIView(views.APIView):
    serializer_class = BillsSerializer
    choice = 'V'
    msg_list = [
        'Bill number {id} already been validated',
        'Bill nro {id} validated successfully for investor {investor_name}'
    ]

    def get_queryset(self, bill):
        queryset = self.serializer_class.Meta.model.objects.filter(
            id=bill
        ).first()
        return queryset
    
    @swagger_auto_schema(manual_parameters=[bill_id],tags=['fees states verification'])
    def get(self, request, *args, **kwargs):
        bill_param = request.query_params.get('bill')
        if not bill_param:
            return Response({'error':'Missing bill ID in query string'}, status=status.HTTP_400_BAD_REQUEST)
        bill = self.get_queryset(bill_param)
        if not bill:
            return Response({'error': f'Bill with ID {bill_param} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if bill.state == self.choice:
            return Response({'msg': self.msg_list[0].format(id=bill.id)})
        bill.state = self.choice
        bill.save()
        return Response({'msg' : self.msg_list[1].format(id=bill.id, investor_name=bill.investor.__str__())})


class SimulateSendEmailAPIView(SimulateVerificationAPIView):
    choice = 'S'
    msg_list = [
        'Bill number {id} already been sendt',
        'Bill nro {id} sendt successfully to investor {investor_name}'
    ]

    @swagger_auto_schema(manual_parameters=[bill_id],tags=['fees states verification'])
    def get(self, request,*args, **kwargs):
        bill_param = request.query_params.get('bill')
        if not bill_param:
            return Response({'error':'Missing bill ID in query string'}, status=status.HTTP_400_BAD_REQUEST)
        bill = self.get_queryset(bill_param)
        if not bill:
            return Response({'error': f'Bill with ID {bill_param} does not exist'})
        if bill.state in ['G','P','O']:
            return Response({'msg' : 'Bill must be Validated before send'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().get(request, *args, **kwargs)


class SimulatePayAPIView(SimulateVerificationAPIView):
    choice = 'P'
    msg_list = [
        'Bill number {id} already been payed',
        'Bill nro {id} marked as payed successfully for investor {investor_name}'
    ]

class SimulateOverdueAPIView(SimulateVerificationAPIView):
    choice = 'O'

    msg_list = [
        'Bill number {id} already been marked as overdue',
        'Bill nro {id} marked as overdue successfully for investor {investor_name}'
    ]

    @swagger_auto_schema(manual_parameters=[bill_id],tags=['fees states verification'])
    def get(self, request,*args, **kwargs):
        bill_param = request.query_params.get('bill')
        if not bill_param:
            return Response({'error':'Missing bill ID in query string'}, status=status.HTTP_400_BAD_REQUEST)
        bill = self.get_queryset(bill_param)
        if not bill:
            return Response({'error': f'Bill with ID {bill_param} does not exist'})
        if date.today() > bill.cash_call_expire:
            if bill.state == self.choice:
                return Response({'msg': self.msg_list[0].format(id=bill.id)})
            elif bill.state == 'P':
                return Response({'msg': f'Bill number {bill_param} already been payed'})
            else:
                bill.state = self.choice
                bill.save()
                return Response({'msg' : self.msg_list[1].format(id=bill.id, investor_name=bill.investor.__str__())})
        return Response({'msg': 'Bill still to date'})