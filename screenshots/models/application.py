from django.db import models

from . import User
from .mixins import BaseModelMixin


class Application(BaseModelMixin):
    name = models.CharField(max_length=256, unique=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = "applications"

    def __str__(self):
        return self.name
