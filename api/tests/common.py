from rest_framework.authtoken.models import Token

from api.models import HotlineUser
from hotline import utils


def auth_test_user(client, user):
    token = Token.objects.create(
        key=utils.id_generator(size=16),
        user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)


def create_user():
    return HotlineUser.objects.create_user(
        email="mail@mail.com",
        password=utils.id_generator())
