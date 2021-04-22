import string
import random

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django_redis import get_redis_connection
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate

from .models import UserProfile


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = {'error': '用户未激活'}
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = {'error': '用户名或密码错误'}
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class FieldsRequiredModelSerializer(serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)

        request = self.context.get('request')
        require_params = request.query_params.get('require')
        fields = (set(fields) & set(require_params.split(','))) if require_params else fields

        exclude_params = request.query_params.get('exclude')
        fields = (set(fields) - set(exclude_params.split(','))) if exclude_params else fields

        return fields


class UserProfileSerializer(FieldsRequiredModelSerializer):
    code = serializers.CharField(max_length=6, min_length=6, read_only=True)

    class Meta:
        model = UserProfile
        fields = serializers.ALL_FIELDS
        # fields = ('uid', 'username', 'phone', 'email', 'last_login', 'code')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            # 'active_code': {
            #     'write_only': True
            # }
        }

    def validate_password(self, password):
        return make_password(password)

    # def validate(self, attrs):
    #     chars = string.ascii_letters + string.digits
    #     active_code = ''.join(random.sample(chars, 16))
    #     attrs['active_code'] = active_code
    #
    #     code = self.context['request'].data.get('code')
    #     if not code:
    #         raise serializers.ValidationError({'code': 'This field is required.'})
    #     else:
    #         redis_cli = get_redis_connection('sms_code')
    #         phone = attrs.get('phone')
    #         if not phone:
    #             raise serializers.ValidationError({'phone': 'This field is required.'})
    #         else:
    #             sms_code = redis_cli.get('code_' + phone)
    #             if sms_code:
    #                 if code == sms_code.decode():
    #                     return attrs
    #                 else:
    #                     raise serializers.ValidationError({'code': '验证码错误'})
    #             else:
    #                 raise serializers.ValidationError({'code': '验证码已过期'})

    def validate_code(self, code):
        redis_cli = get_redis_connection('sms_code')
        phone = self.context['request'].data.get('phone')
        if not phone:
            raise serializers.ValidationError({'phone': 'This field is required.'})
        else:
            sms_code = redis_cli.get('code_' + phone)
            if sms_code:
                if code == sms_code.decode():
                    return code
                else:
                    raise serializers.ValidationError({'error': '验证码错误'})
            else:
                raise serializers.ValidationError({'error': '验证码已过期'})
