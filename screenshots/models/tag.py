from django.db import models

from . import User
from .mixins import BaseModelMixin


class Tag(BaseModelMixin):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name
