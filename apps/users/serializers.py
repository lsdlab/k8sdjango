from .models import User
from rest_framework import serializers

def mobile_restriction(mobile):
    if not mobile.isdigit() or len(mobile) != 11:
        raise serializers.ValidationError("请输入正确的11位手机号。")
    return mobile


def code_restriction(code):
    if not code.isdigit() or len(code) != 6:
        raise serializers.ValidationError("请输入正确的6位数字验证码。")
    return code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'mobile', 'email', 'username', 'nickname',
                  'is_superuser', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class UserPublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname',)
        read_only_fields = ('id', )


class MobileSigninSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[mobile_restriction])
    code = serializers.CharField(required=True, validators=[code_restriction])


class UsernameSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class MobileAutoSignupSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[mobile_restriction])

class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[mobile_restriction])
    code = serializers.CharField(required=True, validators=[code_restriction])
    new_password = serializers.CharField(required=True)


class MobilePasswordCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[mobile_restriction])
    password = serializers.CharField(required=True)
    code = serializers.CharField(required=True, validators=[code_restriction])


class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
