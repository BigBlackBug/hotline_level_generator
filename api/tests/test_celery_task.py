import mock
from PIL import Image
from django.test import TestCase

from api.models import Level
from api.tasks import generate_level_preview
from api.tests import common
from hotline.utils import get_raw_celery_task


class TestCeleryTasks(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()

        cls.level = Level.objects.create(name='level_one',
                                         creator=cls.default_user)

    @mock.patch('api.tasks.image_generator')
    @mock.patch('api.tasks.generator')
    def test_generate_preview(self, mock_generator, mock_image_generator):
        generate = get_raw_celery_task(generate_level_preview)

        mock_generator.generate.return_value = []
        new_image = Image.new('RGBA', (100, 100))
        mock_image_generator.make_image.return_value = new_image

        level_config = {
            'max_width': 234,
            'max_height': 153,
            'room_number': 3
        }
        generate(self.level.id, level_config)
        level = Level.objects.get(pk=self.level.id)
        # might need a better check
        self.assertEquals(level.image.width, new_image.width)
        self.assertEquals(level.image.height, new_image.height)
