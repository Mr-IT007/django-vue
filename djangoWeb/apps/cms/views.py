from apps.mtauth.models import MTUser
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.mtauth.serializer import UserSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        print(request.data)
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            print(user)
            user.last_login = now()
            user.save()

            user_serializer = UserSerializer(instance=user)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({'token': token, 'user': user_serializer.data, 'msg': 'success'})

        else:
            return Response({'msg': '用户名或密码错误！'})
