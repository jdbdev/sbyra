from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from sbyra_src.racing.choices import (
    CompletionStatusChoice,
    YachtClassChoices,
)
from sbyra_src.racing.managers import (
    ActiveYachtManager,
    DefaultYachtManager,
)

User = settings.AUTH_USER_MODEL


""" 
All models related to yacht racing, including yachts, clubs, events and results. This file contains only models.Model classes. 
Refer to separate files for;

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


class YachtClub(RacingCommon):
    """Yacht Club information - not required for racing functionality"""

    name = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        unique=True,
        help_text=_("enter yacht club name"),
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        help_text=_("web safe url"),
    )


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


class Series(RacingCommon):
    """Series class describing all attributes of a series and linking sets of events"""

    name = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        unique=True,
        help_text=_("enter Series' name"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "series"

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    """Event class describing all attributes of an event. Start times based on Yacht class field"""

    name = models.DateField(blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    start_A = models.TimeField(blank=True, null=True)
    start_B = models.TimeField(blank=True, null=True)
    start_C = models.TimeField(blank=True, null=True)
    notes = models.TextField(
        max_length=200,
        blank=True,
        help_text="Add relevant event comments",
    )
    yachts = models.ManyToManyField(Yacht, through="Result")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "events"

    def __str__(self):
        return str(self.name)


class Result(models.Model):
    """Custom Through table linking Many to Many relationship between Yacht and Event"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    completed_status = models.CharField(
        max_length=3,
        choices=CompletionStatusChoice.choices,
        default="CMP",  # check syntax - use default = choices.CMP?
    )
    finish_time = models.TimeField(blank=True, null=True)
    posted_time = models.TimeField(blank=True, null=True)
    notes = models.TextField(max_length=100, blank=True)

    class Meta:
        ordering = ["-posted_time"]
        unique_together = [["event", "yacht"]]
        verbose_name_plural = "results"

    def __str__(self):
        return f"{self.event}: {self.yacht}"

    @property
    def final_result(self):
        """
        Property returns the yacht's race result based on its class start time, PHRF rating and finish time.
        Returns race result only for active yachts that have completed the event. Returns None for all other yachts.
        """
        completed = self.completed_status
        active_status = self.yacht.is_active
        yacht_class = self.yacht.yacht_class

        if active_status and completed == True:
            if yacht_class == "A" or "A1":
                start_time = self.event.start_A
            elif yacht_class == "B":
                start_time = self.event.start_B
            elif yacht_class == "C":
                start_time = self.event.start_C

            phrf_rating = self.yacht.phrf_rating
            time_delta = start_time - self.finish_time
            race_time = time_delta * phrf_rating
            return race_time
        else:
            return None

    def save(self, *args, **kwargs):
        """override default save() method to capture posted_time by accessing the final_result property"""
        self.posted_time = self.final_result
        super(Result, self).save(*args, **kwargs)
