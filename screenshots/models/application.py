from django.db import models

from .mixins import BaseModelMixin


class Application(BaseModelMixin):
    name = models.CharField(max_length=256, unique=True, null=False)

    class Meta:
        db_table = "applications"

    def __str__(self):
        return self.name
