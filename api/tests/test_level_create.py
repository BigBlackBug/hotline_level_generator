from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Level
from api.tests import common
from api.views import GetLevelsView


class TestLevelCreate(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()

    def test_create_level(self):
        common.auth_test_user(self.client, self.default_user)

        response = self.client.post(reverse(GetLevelsView.view_name), data={
            "level_config": "test_config",
            "name": "level_one",
            "is_public": True
        })
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        level_id = response.data['id']
        level_count = Level.objects.filter(pk=level_id).count()
        self.assertEquals(level_count, 1)

    def test_create_level_unauthorized(self):
        response = self.client.post(reverse(GetLevelsView.view_name), data={
            "level_config": "test_config",
            "name": "level_one",
            "is_public": True
        })
        self.assertEquals(response.status_code,
                          status.HTTP_401_UNAUTHORIZED)
