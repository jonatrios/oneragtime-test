from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_view import (
    BillsGenericViewSet,
    SimulateSendEmailAPIView,
    SimulateVerificationAPIView,
    SimulatePayAPIView,
    SimulateOverdueAPIView,
)

router = DefaultRouter()

router.register(r'bills', BillsGenericViewSet, basename='bills-view-set')

api_view_url = [
    path('send-bill/', SimulateSendEmailAPIView.as_view(), name='send-email-api-view'),
    path('validate-bill/',SimulateVerificationAPIView.as_view(),name='verificate-api-view'),
    path('pay-bill/', SimulatePayAPIView.as_view(), name='pay-api-view'),
    path('overdue-bill/', SimulateOverdueAPIView.as_view(), name='overdue-api-view'),
]

urlpatterns = router.urls + api_view_url
