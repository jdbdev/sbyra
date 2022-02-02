from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

""" 
All models related to yacht racing including yachts, clubs, events and results. This file contains only models.Model 
refer to separate files for;

managers.py (all models.Manager classes)
signals.py (all receiver functions and signals)
choices.py (all related models.TextChoices classes for choice fields)

"""


class Timestamp(models.Model):
    """Abstract class for common time fields"""

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Yacht(Timestamp):
    """Yacht class describing all attributes of an individual yacht"""

    name = models.CharField(max_length=100, blank=False, null=True, unique=True, help_text=_("enter yacht name"))
    slug = models.SlugField(blank=True, null=True, help_text=_("web safe url"))

    class Meta:
        verbose_name_plural = "yachts"

    def __str__(self):
        return self.name


class Event(models.Model):
    pass


class Results(models.Model):
    pass


class YachtClub(Timestamp):
    pass


# SIGNALS


@receiver(pre_save, sender=Yacht)
def slug_pre_save(sender, instance, *args, **kwargs):
    """signal to set slug to match name as web safe url"""
    name = instance.name
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(name)
