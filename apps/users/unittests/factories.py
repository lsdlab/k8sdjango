import uuid
import factory
from faker import Faker
fake = Faker("zh_CN")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: uuid.uuid4())
    username = fake.phone_number()
    mobile = username
    password = factory.Faker(
        'password',
        length=10,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True)
