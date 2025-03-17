from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):

    mpassword = models.CharField(verbose_name='mpassword', blank=True, null=True, max_length=200, default="")
    mobile = models.CharField(verbose_name='mobile', blank=True, null=True, max_length=200, default="")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = 'user manage'
        verbose_name_plural = verbose_name