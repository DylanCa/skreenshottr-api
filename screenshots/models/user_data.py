from django.db import models, IntegrityError
from django.db.models import F, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from screenshots.models import User
from screenshots.models.mixins import BaseModelMixin
from screenshots.models.screenshot import Screenshot


class UserData(BaseModelMixin):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='data')
    screenshot_total_count = models.PositiveIntegerField(default=0)
    screenshot_total_size = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "user_data"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserData.objects.create(owner=instance).save()


@receiver(post_save, sender=Screenshot)
def update_screenshot_total_data(sender, instance, created, **kwargs):
    if created:
        data = instance.owner.data
        data.screenshot_total_count = F('screenshot_total_count') + 1
        data.screenshot_total_size = F('screenshot_total_size') + instance.size
        data.save()


@receiver(post_delete, sender=Screenshot)
def update_screenshot_total_data(sender, instance, **kwargs):
    if hasattr(instance.owner, 'data'):
        data = instance.owner.data

        try:
            data.screenshot_total_count = F('screenshot_total_count') - 1
            data.screenshot_total_size = F('screenshot_total_size') - instance.size
            data.save()
        except IntegrityError as e:
            # Ensuring to recalculate if an error happens
            screenshots = Screenshot.objects.filter(owner=instance.owner)
            data.screenshot_total_count = screenshots.count()
            data.screenshot_total_size = screenshots.aggregate(Sum('size'))['size__sum']
            data.save()
    else:
        UserData.objects.get_or_create(owner=instance.owner)
