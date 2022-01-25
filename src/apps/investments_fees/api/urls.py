from django.urls import path
from .api_views import (UpFrontApiView, MembershipAPIView,YearlyFeesBeforeAPIView, 
                            YearlyFeesAfterAPIView,UpdateMembership,UpdateYearlyFeesBefore, UpdateYearlyFeesAfter)

urlpatterns = [
    path('list-upfront/', UpFrontApiView.as_view(), name='upfront-api-view'),
    path('list-membership/', MembershipAPIView.as_view(), name='membership-api-view'),
    path('list-yearly-before/',YearlyFeesBeforeAPIView.as_view(), name='yearly-before-api-view'),
    path('list-yearly-after/',YearlyFeesAfterAPIView.as_view(), name='yearly-after-api-view'),
    path('update-membership/',UpdateMembership.as_view(), name='update-membership-api-view'),
    path('yearly-update-before/', UpdateYearlyFeesBefore.as_view(), name='yearly-update-before-api-view'),
    path('yearly-update-after/', UpdateYearlyFeesAfter.as_view(), name='yearly-update-after-api-view'),
    ]