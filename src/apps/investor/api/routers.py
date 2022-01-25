from rest_framework.routers import DefaultRouter
from .api_views import InvestorModelViewSet, InvestmentModelViewSet, FeePercentageModelViewSet

router = DefaultRouter()

router.register(r'investor', InvestorModelViewSet, basename='inversor-view-set')
router.register(r'fee-percentage', FeePercentageModelViewSet, basename='inversor-view-set')
router.register(r'investment', InvestmentModelViewSet, basename='investment-view-set')


urlpatterns = router.urls
