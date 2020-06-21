from datetime import datetime

from django.conf import settings
from django.test import TestCase

from api.models import HotlineUser, Level
from api.serializers import LevelSerializer
from api.tests import common
from hotline import utils


class TestLevelSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()

        cls.level = Level.objects.create(name='level_one',
                                         creator=cls.default_user)
        cls.level_data = {
            'level_config': '',
            'name': 'level_one',
            'created_on': datetime.strftime(cls.level.created_on,
                                            settings.DATETIME_FORMAT),
            'image': None,
            'is_public': False,
            'creator': cls.default_user.pk,
            'id': cls.level.id
        }

    def test_serialize_one_level(self):
        serializer = LevelSerializer(instance=self.level)
        self.assertEquals(len(serializer.data), len(self.level_data))
        for item in serializer.data.items():
            self.assertEquals(self.level_data[item[0]], item[1])

    def test_serialize_create_level(self):
        serializer = LevelSerializer(data={
            "level_config": "test_config",
            "name": "level_one",
            "is_public": True
        })

        class Mock:
            pass

        mock = Mock()
        setattr(mock, 'user', self.default_user)

        serializer.context['request'] = mock
        serializer.is_valid()
        new_level = serializer.save()
        self.assertEquals(new_level.level_config, "test_config")
