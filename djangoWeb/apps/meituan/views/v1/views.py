from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from apps.meituan.serializer import MerchantSerializer
from apps.meituan.models import Merchant


class CommonPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'pg'
    page_size_query_param = 'pgsize'


class MerchantViewSet(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    pagination_class = CommonPagination
