from unittest import mock

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

    # @mock.patch('api.tasks.generate_level_preview')
    @mock.patch('api.views.generate_level_preview')
    def test_create_level(self, task_mock):
        common.auth_test_user(self.client, self.default_user)

        response = self.client.post(reverse(GetLevelsView.view_name), data={
            "level_config": {
                "max_width": 300,
                "max_height": 300,
                "room_number": 1
            },
            "name": "level_one",
            "is_public": True
        }, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        level_id = response.data['id']
        level_count = Level.objects.filter(pk=level_id).count()
        self.assertEquals(level_count, 1)
        self.assertTrue(task_mock.delay.called)

    def test_create_level_unauthorized(self):
        response = self.client.post(reverse(GetLevelsView.view_name), data={
            "level_config": {
                "max_width": 300,
                "max_height": 300,
                "room_number": 1
            },
            "name": "level_one",
            "is_public": True
        }, content_type='application/json')
        self.assertEquals(response.status_code,
                          status.HTTP_401_UNAUTHORIZED)
