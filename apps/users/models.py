import io
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response

from .managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile = models.CharField(max_length=11, blank=True, default='')
    nickname = models.CharField(max_length=255, blank=True, default='')
    last_login_ip = models.GenericIPAddressField(
        unpack_ipv4=True, null=True, blank=True)
    ip_joined = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined', ]
        verbose_name = '用户'
        verbose_name_plural = verbose_name


    @classmethod
    def check_user_exist(self, mobile, email):
        existing_mobile = User.objects.filter(
            mobile=mobile).exists()
        existing_email = User.objects.filter(
            email=email).exists()
        if existing_mobile:
            return Response(
                {
                    'mobile': ['手机号已存在'],
                }, status=status.HTTP_400_BAD_REQUEST)
        elif existing_email:
            return Response(
                {
                    'email': ['邮箱已存在'],
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "OK"}, status=status.HTTP_200_OK)
