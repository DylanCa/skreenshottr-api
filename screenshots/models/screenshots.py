import uuid

from django.db import models

from .users import User
from .mixins import BaseModelMixin, DateTimeMixin


class Screenshot(BaseModelMixin, DateTimeMixin):
    file_url = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, default=None)

    class Meta:
        db_table = "screenshots"

    def __str__(self):
        return self.file_url
