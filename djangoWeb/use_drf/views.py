from rest_framework import viewsets
from meituan.models import Merchant, GoodsCategory, Goods
from .serializer import MerchantSerializer, GoodsCategorySerializer, GoodsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

    # authentication_classes = []
    # permission_classes = []

    @action(methods=['GET'], detail=False, url_path='cs')
    def contain_cs(self, request):
        # queryset = self.get_queryset()
        queryset = self.queryset.filter(name__contains='长沙')
        # serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GoodsCategoryViewSet(viewsets.ModelViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer


class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
