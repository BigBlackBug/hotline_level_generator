# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import HotlineUser, Level
from api.serializers import LevelSerializer
from api.tests import common
from api.views import GetLevelsView
from hotline import utils


class TestLevelsCRUD(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.default_user = common.create_user()

        cls.public_level = Level.objects.create(name='public_level',
                                                is_public=True,
                                                creator=cls.default_user)
        cls.private_level = Level.objects.create(name='private_level',
                                                 creator=cls.default_user)

    def test_get_levels(self):
        resp = self.client.get(reverse(GetLevelsView.view_name))
        data = resp.data
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(data), 1)
        level = self.public_level
        data = data[0]
        serializer = LevelSerializer(instance=level)
        self.assertEquals(data, serializer.data)
