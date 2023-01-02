from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    creation_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    def __str__(self) -> str:
        return self.name
