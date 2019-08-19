import base64
from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from apps.users.unittests.factories import UserFactory
from apps.users.models import User


class TestUsersEmailPasswordPostCreateAPI(APITestCase):
    def setUp(self):
        self.url = reverse('users:user-email_password_signup')
        self.user_data = {
            "email": "julian_chen@amaxchina.com",
            "password": "julian_chen"
        }

    def test_post_with_valid_data_success(self):
        # 邮箱创建用户成功
        response = self.client.post(self.url, self.user_data, format='json')
        eq_(response.status_code, 201)
        user = User.objects.get(pk=response.data.get('id'))
        ok_(check_password(self.user_data.get('password'), user.password))
        eq_(self.user_data.get('email'), user.email)

        # 创建重复邮箱用户
        response = self.client.post(self.url, self.user_data, format='json')
        eq_(response.status_code, 400)
        eq_(response.json()['email'], ["邮箱已存在"])

    def test_post_with_empty_email_fail(self):
        # 空邮箱
        wrong_data = self.user_data
        del wrong_data['email']
        response = self.client.post(
            self.url, wrong_data, format='json')
        eq_(response.status_code, 400)
        eq_(response.json()['email'], ['This field is required.'])

    def test_post_with_wrong_email_fail(self):
        # 错误邮箱格式
        wrong_data = {
            "email": "lsdvincent",
            "password": "julian_chen"
        }
        response = self.client.post(
            self.url, wrong_data, format='json')
        eq_(response.status_code, 400)


class TestUsersGetListAndObjectAPI(APITestCase):
    def signup(self):
        # 注册 superuser 获取 token
        self.user_data = model_to_dict(UserFactory.build())
        user = User.objects.create_user(
            username=self.user_data.get('username'),
            mobile=self.user_data.get('mobile'),
            password=self.user_data.get('password'),
            is_superuser=True)
        user.save()
        self.user = User.objects.get(pk=user.id)
        token_auth_url = reverse('users:user-username_password_signin')
        data = {
            'username': self.user.username,
            'password': self.user_data.get('password')
        }
        response = self.client.post(token_auth_url, data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

    def setUp(self):
        self.signup()
        self.user_list_url = reverse('users:user-list')
        self.single_user_url = reverse(
            'users:user-detail', kwargs={'pk': str(self.user.id)})
        self.current_user_url = reverse('users:user-current_user')

    def test_get_users_list(self):
        # 获取用户 list
        response = self.client.get(self.user_list_url)
        eq_(response.status_code, 200)

    def test_get_single_user(self):
        # 获取单个用户
        response = self.client.get(self.single_user_url)
        eq_(response.status_code, 200)

    def test_get_current_user(self):
        # 获取当前 token 的用户
        response = self.client.get(self.current_user_url)
        eq_(response.status_code, 200)

    def test_patch_update_signle_user(self):
        # patch 修改当前用户
        patch_user_data = {"weixin_userinfo": {'nickName': 'xxxx'}}
        response = self.client.patch(
            self.single_user_url, patch_user_data, format='json')
        eq_(response.status_code, 200)

    def test_delete_signle_user(self):
        # destroy 删除当前用户
        response = self.client.delete(self.single_user_url)
        eq_(response.status_code, 204)


class TestUserTokenAPI(APITestCase):
    def signup(self):
        self.url = reverse('users:user-email_password_signup')
        self.user_data = {
            "email": "julian_chen@amaxchina.com",
            "password": "123456789"
        }
        response = self.client.post(
            self.url, self.user_data, format='json')
        eq_(response.status_code, 201)

    def setUp(self):
        self.signup()
        self.username_password_signin_url = reverse(
            'users:user-username_password_signin')
        self.username_password_signin_data = {
            "username": "julian_chen",
            "password": "123456789"
        }

    def test_username_password_signin_success(self):
        # username/password 获取token
        response = self.client.post(
            self.username_password_signin_url, self.username_password_signin_data, format='json')
        eq_(response.status_code, 200)

    def test_username_password_signin_empty_username(self):
        # username/password 空username
        wrong_data = self.username_password_signin_data
        del wrong_data['username']
        response = self.client.post(
            self.username_password_signin_url,
            wrong_data,
            format='json')
        eq_(response.status_code, 400)
        eq_(response.json()['username'], ['This field is required.'])

    def test_username_password_signin_wrong_username(self):
        # username/password 错误username
        wrong_data = {"username": "roo", "password": "root"}
        response = self.client.post(
            self.username_password_signin_url,
            wrong_data,
            format='json')
        eq_(response.status_code, 400)
        eq_(response.json()['detail'], '用户名或密码错误')

