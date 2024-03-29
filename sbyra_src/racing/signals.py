from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Yacht, YachtClub

# --------------------- MODEL: Yacht --------------------- #


@receiver(pre_save, sender=Yacht)
def slug_pre_save(sender, instance, *args, **kwargs):
    """signal sets slug to match name as a web safe url"""
    name = instance.yacht_name
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(name)


@receiver(pre_save, sender=Yacht)
def yacht_is_active(sender, instance, *args, **kwargs):
    """sets is_active = True when instance has phrf_rating and yacht_class values at creation or update"""
    if instance.phrf_rating is not None:
        if instance.yacht_class is not None:
            instance.is_active = True


# ------------------- MODEL: YachtClub ------------------- #


@receiver(pre_save, sender=YachtClub)
def slug_pre_save(sender, instance, *args, **kwargs):
    """Signal sets slug to match name as a web safe url. Updating name will result in updated slug"""
    name = instance.yacht_club_name
    instance.slug = slugify(name)
