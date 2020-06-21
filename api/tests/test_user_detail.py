# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Level
from api.serializers import UserSerializer
from api.tests import common
from api.views import GetUserDetailView


class TestUserDetail(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.default_user = common.create_user()
        Level.objects.create(name='public_level',
                             is_public=True,
                             creator=cls.default_user)
        Level.objects.create(name='private_level',
                             is_public=True,
                             creator=cls.default_user)

    def test_get_one_user(self):
        resp = self.client.get(
            reverse(GetUserDetailView.view_name, kwargs={
                'pk': self.default_user.id
            }))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        real_data = UserSerializer(instance=self.default_user).data
        self.assertEquals(real_data, resp.data)
