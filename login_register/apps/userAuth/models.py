from datetime import datetime

from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    uid = ShortUUIDField(primary_key=True, verbose_name='用户主键')
    # is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    phone = models.CharField(unique=True, max_length=11, verbose_name='手机号')
    email = models.EmailField(unique=True, max_length=100, verbose_name='邮箱')
    avatar = models.URLField(max_length=200, null=True, blank=True, verbose_name='头像链接')
    register_time = models.DateTimeField(default=datetime.now, verbose_name='注册时间')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    active_code = models.CharField(max_length=16, null=True, blank=True, verbose_name='激活码')
    active_time = models.DateTimeField(null=True, blank=True, verbose_name='激活时间')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Key(models.Model):
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='开发者')
    app = models.CharField(max_length=20, verbose_name='应用')
    key = models.CharField(max_length=32, verbose_name='应用key值')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = 'key值表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.key


# class SMSCode(models.Model):
#     phone = models.CharField(max_length=11, verbose_name='手机号')
#     code = models.CharField(max_length=6, verbose_name='验证码')
#     send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
#     expire = models.DateTimeField(default=datetime.now, verbose_name='过期时间')
#
#     class Meta:
#         verbose_name = '短信验证码表'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.phone
