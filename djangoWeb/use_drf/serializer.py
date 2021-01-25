from rest_framework import serializers
from meituan.models import Merchant, GoodsCategory, Goods


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'
        # exclude = ['name']


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


# 序列化嵌套
class GoodsCategorySerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True)
    merchant_id = serializers.IntegerField(write_only=True)
    goods_list = GoodsSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'

    def validate_merchant_id(self, value):
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError('The id you submit is not exist!')

        return value
