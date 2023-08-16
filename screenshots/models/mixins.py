import uuid
from datetime import datetime

from django.db import models
from django.db.models import Manager, QuerySet


class BaseManagerMixin(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(deleted_at__isnull=False)


class BaseModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    objects = BaseManagerMixin()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.utcnow()
        self.save()
