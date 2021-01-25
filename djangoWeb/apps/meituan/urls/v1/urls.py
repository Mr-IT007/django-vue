from rest_framework.routers import DefaultRouter
from apps.meituan.views.v1.views import MerchantViewSet


router = DefaultRouter()
router.register('merchant', MerchantViewSet, base_name='merchant')

urlpatterns = [] + router.urls
