import datetime
import random

from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework_jwt.views import jwt_response_payload_handler

from djangoWeb.settings import API_KEY
from apps.userAuth.utils import SendMessage
from apps.userAuth.models import UserProfile
from apps.userAuth.serializer import UserProfileSerializer, JWTSerializer


class CommonPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'pg'
    page_size_query_param = 'ps'


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = CommonPagination
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    @action(methods=['post'], detail=False, authentication_classes=(), permission_classes=())
    def login(self, request):
        serializer = JWTSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.object.get('user')
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)

            return Response(response_data, 200)

    @action(methods=['post'], detail=False, authentication_classes=(), permission_classes=())
    def register(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            msg = '注册成功'
            data = {
                'code': 201,
                'data': {
                    'msg': msg
                }
            }

            return Response(data, 201)

    @action(methods=['get'], detail=False, authentication_classes=(), permission_classes=())
    def active(self, request):
        active_code = request.query_params.get('code')
        if not active_code:
            msg = '请使用激活码激活'
            data = {
                'code': 400,
                'data': {'msg': msg}
            }

            return Response(data, 400)
        else:
            user = self.queryset.filter(active_code=active_code).last()
            if not user:
                msg = '激活码无效'
                data = {
                    'code': 400,
                    'data': {'msg': msg}
                }

                return Response(data, 400)
            else:
                user.is_active = True
                user.active_time = datetime.datetime.now()
                user.save()

                msg = '激活成功'
                data = {
                    'code': 200,
                    'data': {'msg': msg}
                }

                return Response(data, 200)


# class RegisterView(APIView):
#     authentication_classes = ()
#     permission_classes = ()
#
#     def post(self, request):
#         serializer = UserProfileSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             msg = '注册成功'
#             data = {
#                 'code': 201,
#                 'data': {
#                     'msg': msg
#                 }
#             }
#
#             return Response(data, 201)


class SendCodeView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        phone = request.query_params.get('phone')
        if phone:
            is_registered = UserProfile.objects.filter(phone=phone).exists()
            if is_registered:
                msg = '手机号已被注册'
                data = {
                    'code': 402,
                    'data': {'msg': msg}
                }

                return Response(data, 402)
            else:
                redis_cli = get_redis_connection('sms_code')
                sms_code = redis_cli.get('code_' + phone)
                send_counts = redis_cli.get('counts_' + phone)

                if sms_code:
                    msg = '距上次发送验证码不足2分钟'
                    data = {
                        'code': 403,
                        'data': {'msg': msg}
                    }

                    return Response(data, 403)

                else:
                    if send_counts:
                        if int(send_counts) < 10:
                            code = random.randint(100000, 999999)
                            redis_cli.setex('code_' + phone, 120, code)
                            redis_cli.incr('counts_' + phone)

                            sms_send = SendMessage(API_KEY)
                            result = sms_send.send_sms(code, phone)

                            return Response(result)
                        else:
                            msg = '当天短信发送次数已超上限'
                            data = {
                                'code': 403,
                                'data': {'msg': msg}
                            }

                            return Response(data, 403)
                    else:
                        current_time = datetime.datetime.now().replace(microsecond=0)
                        expire_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 6, 0, 0) + datetime.timedelta(days=1)

                        code = random.randint(100000, 999999)
                        redis_cli.setex('code_' + phone, 120, code)
                        redis_cli.setex('counts_' + phone, (expire_time - current_time).seconds, 1)

                        sms_send = SendMessage(API_KEY)
                        result = sms_send.send_sms(code, phone)

                        return Response(result)

        else:
            msg = '手机号为空'
            data = {
                'code': 400,
                'data': {'msg': msg}
            }

            return Response(data, 400)


# class ActiveView(APIView):
#     authentication_classes = ()
#     permission_classes = ()
#
#     def get(self, request):
#         active_code = request.query_params.get('code')
#         if not active_code:
#             msg = '请使用激活码激活'
#             data = {
#                 'code': 400,
#                 'data': {'msg': msg}
#             }
#
#             return Response(data, 400)
#         else:
#             user = UserProfile.objects.filter(active_code=active_code).last()
#             if not user:
#                 msg = '激活码无效'
#                 data = {
#                     'code': 400,
#                     'data': {'msg': msg}
#                 }
#
#                 return Response(data, 400)
#             else:
#                 user.is_active = True
#                 user.active_time = datetime.datetime.now()
#                 user.save()
#
#                 msg = '激活成功'
#                 data = {
#                     'code': 200,
#                     'data': {'msg': msg}
#                 }
#
#                 return Response(data, 200)
