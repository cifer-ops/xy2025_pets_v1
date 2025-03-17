from django.db import models
from accounts.models import UserProfile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class PetsType(models.Model):
    name = models.CharField(max_length=1024, verbose_name="type name")
    updated = models.DateTimeField(auto_now=True, verbose_name='modify')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='created')

    class Meta:
        verbose_name = 'PetsType'
        verbose_name_plural = 'PetsType'

    def __str__(self):
        return self.name


class PetsInfo(models.Model):
    CHOICES = (
        ('0', 'release'),
        ('1', 'adopted person selected'),
        ('2', 'adopted'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    showimg = models.ImageField(blank=True, null=True, verbose_name='show image', upload_to="image/")
    name = models.CharField(max_length=1024, verbose_name="name")
    intro = RichTextUploadingField(verbose_name="introduce")
    area = models.CharField(max_length=1024, verbose_name="area")
    atype = models.ForeignKey(PetsType, verbose_name="type", on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name='age', default=0)
    status = models.CharField(max_length=1024, verbose_name="status", default="0", choices=CHOICES)
    updated = models.DateTimeField(auto_now=True, verbose_name='updated')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')

    class Meta:
        verbose_name = 'PetsInfo'
        verbose_name_plural = 'PetsInfo'

    def __str__(self):
        return self.name


class Collect(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pet = models.ForeignKey(PetsInfo, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, verbose_name='updated')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')

    class Meta:
        verbose_name = 'Collect'
        verbose_name_plural = 'Collect'

    def __str__(self):
        return str(self.user)


class Adoption(models.Model):
    CHOICES = (
        ('0', 'registered'),
        ('1', 'passed'),
        ('2', 'adopted'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pet = models.ForeignKey(PetsInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=1024, verbose_name="status", default="0", choices=CHOICES)
    updated = models.DateTimeField(auto_now=True, verbose_name='updated')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')

    class Meta:
        verbose_name = 'adoption'
        verbose_name_plural = 'adoption'

    def __str__(self):
        return str(self.user)
