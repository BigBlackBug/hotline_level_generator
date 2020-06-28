from datetime import datetime

from PIL import Image
from django.conf import settings
from django.test import TestCase
from mock import MagicMock

from api.models import Level
from api.serializers import LevelSerializer
from api.tests import common


class TestLevelSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()

        cls.level = Level.objects.create(name='level_one',
                                         creator=cls.default_user)
        cls.level_data = {
            'level_config': None,
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
            "level_config": None,
            "name": "level_one",
            "is_public": True
        })

        serializer.context['request'] = MagicMock(user=self.default_user)
        serializer.is_valid(raise_exception=True)
        new_level = serializer.save()
        self.assertEquals(new_level.name, "level_one")


class TestLevelModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()

        cls.level = Level.objects.create(name='level_one',
                                         creator=cls.default_user)

    def test_save_image(self):
        self.assertFalse(self.level.image)
        image = Image.new('RGBA', (250, 250), 'blue')
        self.level.add_image(image)
        saved_image = self.level.image
        self.assertTrue(saved_image.name)
