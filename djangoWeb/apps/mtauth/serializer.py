from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import exceptions

from .models import MTUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTUser
        # exclude = ('password',)
        fields = serializers.ALL_FIELDS

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_password(self, password):
        return make_password(password)
