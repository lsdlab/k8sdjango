import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.settings import api_settings
from .models import User
from .serializers import (
    UserSerializer,
    EmailPasswordSerializer,
    UsernameSigninSerializer,
    UserChangePasswordSerializer,
    UserResetPasswordSerializer,
)
from .permissions import IsCreationOrIsAuthenticated, IsOwn
from apps.core.serializers import EmptySerializer
from apps.core.patch_only_mixin import PatchOnlyMixin
from apps.core.utils import get_user_ip


def log_user_ip(request, user):
    ip = get_user_ip(request)
    user.last_login_ip = ip
    if user.ip_joined:
        user.ip_joined += ip + ','
    else:
        user.ip_joined = ip + ','
    user.save()


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  PatchOnlyMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    用户增删改查
    get list(admin only)/create(all user)/retrieve(admin only)
    patch(all)/destroy(admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreationOrIsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'email_password_signup':
            return EmailPasswordSerializer
        elif self.action == 'username_password_signin':
            return UsernameSigninSerializer
        elif self.action == 'change_password':
            return UserChangePasswordSerializer
        elif self.action == 'reset_password':
            return UserResetPasswordSerializer
        elif self.action == 'current_user':
            return UserSerializer
        else:
            return UserSerializer

    def list(self, request):
        """
        get(list) 列表
        url params: search(username/mobile/email)
        """
        search = request.query_params.get('search')
        filter_condition = Q()
        if search:
            filter_condition = filter_condition & Q(
                username__icontains=search) | Q(mobile__icontains=search) | Q(
                    email__icontains=search)
        queryset = User.objects.filter(filter_condition)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        假删除 deleted -> True, is_active -> False
        """
        user = self.get_object()
        user.is_active = False
        user.deleted = True
        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=False,
        url_path='email_password_signup',
        url_name='email_password_signup',
        serializer_class=EmailPasswordSerializer,
        permission_classes=[
            AllowAny,
        ])
    def email_password_signup(self, request):
        """
        邮箱新增用户 email/password 必填
        {
            "email": "string@string.com",
            "password": "string"
        }
        """

        serializer = EmailPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            exist_status = User.check_user_exist(mobile=None, email=email)
            if exist_status.status_code == 400:
                return exist_status
            else:
                user = User.objects.create_user(
                    email=email,
                    username=email.split('@')[0],
                    password=password)
                user.save()
                user.refresh_from_db()
                user_serializer = UserSerializer(
                    user, many=False, context={"request": request})
                return Response(
                    user_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['post'],
        detail=False,
        url_path='username_password_signin',
        url_name='username_password_signin',
        serializer_class=UsernameSigninSerializer,
        permission_classes=[
            AllowAny,
        ])
    def username_password_signin(self, request):
        """
        用户名和密码登录获取 token
        username/password 必填，用户名和密码登录获取 token
        {
            "username": "",
            "password": ""
        }
        """
        serializer = UsernameSigninSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            authenticated_user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'])
            if authenticated_user:
                # log user ip
                log_user_ip(request, authenticated_user)
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(authenticated_user)
                token = jwt_encode_handler(payload)
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "detail": "用户名或密码错误"
                    }, status=status.HTTP_400_BAD_REQUEST)


    @action(
        methods=['get'],
        detail=False,
        url_name='current_user',
        url_path='current_user',
        serializer_class=UserSerializer,
        permission_classes=[
            IsAuthenticated,
        ])
    def current_user(self, request):
        """
        用 token 获取当前用户信息，需要 token
        """
        current_user = request.user
        result = UserSerializer(
            current_user, many=False, context={'request': request})
        return Response(result.data, status=status.HTTP_200_OK)
