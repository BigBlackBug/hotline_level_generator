from django.contrib.auth.models import AbstractBaseUser, AbstractUser
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
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    # TODO make it a jsonfield
    level_config = models.TextField(max_length=1024, default="")
    name = models.CharField(max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', blank=True)
    is_public = models.BooleanField(default=False)
    creator = models.ForeignKey(HotlineUser, on_delete=models.CASCADE,
                                related_name='levels',
                                related_query_name='level')
