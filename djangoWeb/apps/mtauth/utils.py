from .serializer import UserSerializer
from .models import MTUser
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.utils.timezone import now


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :token  返回的jwt
    :user   当前登录的用户信息[对象]
    :request 当前本次客户端提交过来的数据
    """

    return {
        'token': token,
        'data': {'user': UserSerializer(instance=user).data},
        'msg': 'success',
        'code': 20000
    }


class UsernameMobileAuthBackend(ModelBackend):
    """用户名或手机登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """判断用户名(手机号码)和密码是否正确"""
        query_set = MTUser.objects.filter(Q(username=username) | Q(telephone=username))
        try:
            if query_set.exists():
                user = query_set.get()
                if user.check_password(password):
                    user.last_login = now()
                    user.save()
                    return user
        except:
            return None
