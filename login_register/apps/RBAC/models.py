from django.db import models


class Permission(models.Model):
    permission_desc = models.CharField(max_length=20, verbose_name='权限描述')

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.permission_desc


class Role(models.Model):
    role = models.CharField(max_length=20, verbose_name='角色名')
    permission = models.ManyToManyField(Permission, null=True, blank=True)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    role = models.ManyToManyField(Role, null=True, blank=True)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
