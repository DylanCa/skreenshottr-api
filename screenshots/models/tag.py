from django.db import models

from .mixins import BaseModelMixin


class Tag(BaseModelMixin):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name
