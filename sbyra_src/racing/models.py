from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from sbyra_src.racing.choices import YachtClassChoices
from sbyra_src.racing.managers import (
    ActiveYachtManager,
    DefaultYachtManager,
)

User = settings.AUTH_USER_MODEL


""" 
All models related to yacht racing including yachts, clubs, events and results. This file contains only models.Model 
refer to separate files for;

managers.py (all models.Manager classes and custom methods)
signals.py (all receiver functions and signals)
choices.py (all related models.TextChoices classes for choice fields)

Any changes to models to remain explicit and include help_text.

"""


class RacingCommon(models.Model):
    """Abstract class for common time fields. Use for all models"""

    created = models.DateTimeField(
        auto_now_add=True, null=True
    )  # null=True temporary only for testing
    updated = models.DateTimeField(
        auto_now=True, null=True
    )  # null=True temporary only for testing

    class Meta:
        abstract = True


class Yacht(RacingCommon):
    """Yacht class describing all attributes of an individual yacht"""

    name = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        unique=True,
        help_text=_("enter yacht name"),
    )
    slug = models.SlugField(
        blank=True, null=True, help_text=_("web safe url")
    )
    yacht_class = models.CharField(
        max_length=2,
        choices=YachtClassChoices.choices,
        blank=True,
        null=True,
        help_text=_("yacht class required to race"),
    )
    phrf_rating = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("phrf rating required to race"),
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_("requires phrf rating and yacht class"),
    )

    objects = DefaultYachtManager()  # Yacht.objects.all()
    active = ActiveYachtManager()  # Yacht.active.all()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "yachts"

    def __str__(self):
        return self.name


class Event(models.Model):
    pass


class Results(models.Model):
    pass


class YachtClub(RacingCommon):
    pass
