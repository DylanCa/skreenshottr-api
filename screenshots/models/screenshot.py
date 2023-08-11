from django.db import models

from .tag import Tag
from .mixins import BaseModelMixin


class Screenshot(BaseModelMixin):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=256, null=True)
    image_url = models.URLField(max_length=256)
    thumbnail_url = models.URLField(max_length=256)
    filename = models.CharField(max_length=128)
    tags = models.ManyToManyField(Tag, default=None)

    format = models.CharField(max_length=8)
    size = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        db_table = "screenshots"

    def __str__(self):
        return self.name
