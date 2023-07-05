import uuid

from django.db import models

from .mixins import BaseModelMixin, DateTimeMixin


class User(BaseModelMixin, DateTimeMixin):
    username = models.CharField(max_length=24, null=False, unique=True)
    name = models.CharField(max_length=24, null=True, blank=False)
    surname = models.CharField(max_length=24, null=True, blank=False)
    email = models.EmailField(max_length=254, null=False, unique=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
