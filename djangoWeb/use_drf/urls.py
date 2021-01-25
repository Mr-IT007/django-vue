from rest_framework.routers import DefaultRouter
from .views import MerchantViewSet, GoodsCategoryViewSet, GoodsViewSet


app_name = 'use_drf'

router = DefaultRouter()
router.register('v1/merchant', MerchantViewSet, base_name='merchant')
router.register('v1/goodscategory', GoodsCategoryViewSet, base_name='goodscategory')
router.register('v1/goods', GoodsViewSet, base_name='goods')

urlpatterns = [] + router.urls
