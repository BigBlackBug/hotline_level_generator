from io import BytesIO

from PIL.Image import Image
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.postgres.fields import JSONField
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class HotlineUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Level(models.Model):
    _DEFAULT_IMAGE_FORMAT = 'png'

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    # TODO make it a jsonfield
    level_config = JSONField(max_length=1024, blank=True, null=True)
    name = models.CharField(max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', blank=True)
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey(HotlineUser, on_delete=models.CASCADE,
                                related_name='levels',
                                related_query_name='level')

    def add_image(self, image: Image):
        image_file = BytesIO()
        image.save(image_file, self._DEFAULT_IMAGE_FORMAT)
        self.image.save(
            f"{self.name}_level.{self._DEFAULT_IMAGE_FORMAT}",
            ContentFile(image_file.getvalue())
        )
