from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from apps.users.unittests.factories import UserFactory
from apps.users.serializers import UserSerializer


class TestUsersSerializer(TestCase):

    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = UserSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = UserSerializer(data=self.user_data)
        ok_(serializer.is_valid())
