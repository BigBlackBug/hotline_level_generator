from django.test import TestCase

from django.test import TestCase

from api.models import Level
from api.serializers import LevelSerializer, UserSerializer
from api.tests import common


class TestUserSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = common.create_user()
        cls.level = Level.objects.create(name='level_one',
                                         is_public=True,
                                         creator=cls.default_user)
        cls.level_2 = Level.objects.create(name='level_two',
                                           is_public=False,
                                           creator=cls.default_user)
        # userserializer should return only public levels
        serializer = LevelSerializer(instance=[cls.level],
                                     many=True)
        cls.user_data = {
            'email': cls.default_user.email,
            'levels': serializer.data,
            'id': cls.default_user.id
        }

    def test_serialize_user(self):
        serializer = UserSerializer(instance=self.default_user)
        self.assertEquals(len(serializer.data), len(self.user_data))
        for item in serializer.data.items():
            self.assertEquals(self.user_data[item[0]], item[1])
