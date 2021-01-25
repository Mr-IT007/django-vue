from rest_framework.serializers import ModelSerializer
from .models import Merchant


class MerchantSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        # fields = '__all__'
        fields = ['name', 'address', 'logo', 'notice', 'up_send', 'lon', 'lat', 'create_time', 'creator', 'url']
