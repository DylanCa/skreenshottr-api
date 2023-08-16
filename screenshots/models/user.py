from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
