import requests
import datetime

from django.core.mail import send_mail
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.views import exception_handler

from djangoWeb.settings import DEFAULT_FROM_EMAIL
from .serializer import UserProfileSerializer
from .models import UserProfile


def define_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        response.data = {
            'code': exc.status_code,
            'msg': exc.detail
        }
    return response


class SendMessage(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        data = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': f'【王佳吉敏】您的验证码是{code}，有效期为30分钟，请勿在10分钟内反复发送。如非本人操作，请忽略本短信'
        }

        r = requests.post(self.single_send_url, data=data)
        return r.json()


def send_email(email, code):
    email_title = '注册激活链接'
    email_content = f'点击链接激活你的帐号：http://127.0.0.1:8000/api/v1/user/active?code={code}'
    send_mail(email_title, email_content, DEFAULT_FROM_EMAIL, [email])


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'code': 200,
        'token': token,
        'data': {
            'user': UserProfileSerializer(instance=user, context={'request': request}).data,
            'msg': 'success'
        }
    }


class UsernameMobileAuthBackend(ModelBackend):
    """用户名或手机登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = UserProfile.objects.filter(Q(username=username) | Q(phone=username)).first()
        try:
            if user:
                if user.check_password(password):
                    user.last_login = datetime.datetime.now()
                    user.save()
                    return user
        except:
            return None


if __name__ == '__main__':
    msg = SendMessage('65fccca60635bde9e728a3e4a9361a82')
    result = msg.send_sms(696969, '17709608161')
    print(result)
