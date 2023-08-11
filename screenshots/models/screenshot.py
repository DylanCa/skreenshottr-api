from django.db import models

from .tag import Tag
from .mixins import BaseModelMixin


class Screenshot(BaseModelMixin):
    name = models.CharField(max_length=128)
    file_url = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, default=None)

    class Meta:
        db_table = "screenshots"

    def __str__(self):
        return self.name
