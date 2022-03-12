import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from sbyra_src.racing.choices import (
    CompletionStatusChoice,
    YachtClassChoices,
)
from sbyra_src.racing.managers import (
    ActiveYachtManager,
    CurrentYearSeriesManager,
    DefaultSeriesManager,
    DefaultYachtManager,
)

from .validators import validate_year

User = settings.AUTH_USER_MODEL


""" 
All models related to yacht racing, including yachts, clubs, events and results. This file contains only models.Model classes. 
Refer to separate files for;

managers.py (all models.Manager classes and custom methods)
signals.py (all receiver functions and signals)
choices.py (all related models.TextChoices classes for choice fields)
validators.py (additional data validation functions)

Any changes to models to remain explicit and include help_text.

"""


class RacingCommon(models.Model):
    """Abstract class for common time fields used in all other model classes"""

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
        blank=True,
        null=True,
        help_text=_("web safe url"),
        verbose_name="Web safe URL",
    )
    sail_num = models.CharField(
        max_length=25,
        blank=True,
        help_text=_("Main sail number"),
        verbose_name="sail number",
    )
    yacht_type = models.CharField(
        max_length=50, blank=True, help_text=_("Type of yacht")
    )
    yacht_class = models.CharField(
        max_length=2,
        choices=YachtClassChoices.choices,
        blank=True,
        null=True,
        help_text=_("required to race"),
    )
    phrf_rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        help_text=_("required to race"),
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
        verbose_name="Series Name",
        help_text=_("Example: Weekly Regatta"),
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Format: 2020"),
        validators=[validate_year],
    )
    current_year = models.BooleanField(
        default=True, help_text=_("archived if not current year")
    )
    notes = models.TextField(
        max_length=500, help_text=_("maximum 500 characters")
    )

    objects = DefaultSeriesManager()
    current = CurrentYearSeriesManager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "series"

    def __str__(self):
        return f"{self.name} {self.year}"

    def save(self, *args, **kwargs):
        t_now = datetime.datetime.now()
        t1 = self.year
        t2 = t_now.year
        if t1 < t2:
            self.current_year = False
        super(Series, self).save(*args, **kwargs)


class Event(RacingCommon):
    """Event class describing all attributes of an event. Start times based on Yacht class field"""

    event_date = models.DateField(blank=True)
    series = models.ForeignKey(
        Series, related_name="events", on_delete=models.CASCADE
    )
    first_flag_A = models.TimeField(blank=True, null=True)
    first_flag_B = models.TimeField(blank=True, null=True)
    first_flag_C = models.TimeField(blank=True, null=True)
    start_A = models.TimeField(blank=True, null=True)
    start_B = models.TimeField(blank=True, null=True)
    start_C = models.TimeField(blank=True, null=True)
    start_J = models.TimeField(blank=True, null=True)
    notes = models.TextField(
        max_length=200,
        blank=True,
        help_text="Add relevant event comments",
    )
    yachts = models.ManyToManyField(Yacht, through="Result")

    class Meta:
        ordering = ["event_date"]
        verbose_name_plural = "events"

    def __str__(self):
        return str(self.name)


class Result(RacingCommon):
    """Custom Through table linking Many to Many relationship between Yacht and Event"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    completed_status = models.CharField(
        max_length=3,
        choices=CompletionStatusChoice.choices,
        default="CMP",
        help_text=_("race completion status"),
    )
    finish_time = models.TimeField(
        blank=True, null=True, help_text=_("Format: HH:MM:SS")
    )
    over_line = models.IntegerField()
    time_penalty = models.TimeField(
        blank=True, null=True, help_text=_("Format: HH:MM:SS")
    )
    posted_time = models.TimeField(
        blank=True,
        null=True,
        help_text=_("Format: HH:MM:SS"),
    )
    notes = models.TextField(
        max_length=100, blank=True, help_text=_("add any result notes")
    )

    class Meta:
        ordering = ["-posted_time"]
        unique_together = [["event", "yacht"]]
        verbose_name_plural = "results"

    def __str__(self):
        return f"{self.event}: {self.yacht}"

    @property
    def yacht_class_start(self):
        """Returns racing class start time for a specific yacht in a specific event based on yacht racing class"""
        yacht_class = self.yacht.yacht_class
        if yacht_class == "A" or "A1":
            class_start = self.event.start_A
        elif yacht_class == "B":
            class_start = self.event.start_B
        elif yacht_class == "C":
            class_start = self.event.start_C
        elif yacht_class == "J":
            class_start = self.event.start_J
        return class_start

    @property
    def calc_corrected_time(self):
        """
        Returns the yacht's corrected time based on its elapsed time and time correction factor, and applies any penalties.
        Returns result only for active yachts that have completed the event. Returns None for all other yachts.

        sbyra time correction factor used: 650/(520 + phrf_rating)

        Corrected Time Algorithm:

        1. Establish start time based on yach's racing class and event's corresponding start time
        2. Convert start time and finish time to seconds for further processing
        3. Calculate elapsed time in seconds between start time and finish time
        4. Apply time correction factor based on phrf_rating and known formula
        5. Convert corrected time above (seconds) into datetime.time object for model TimeField()
        6. Save final datetime.time object into Result.posted_time

        """

        def convert_to_seconds(time_obj) -> int:
            """Function takes a datetime.time object and converts into seconds"""
            seconds = (
                (time_obj.hour * 3600)
                + (time_obj.minute * 60)
                + (time_obj.second)
            )
            return seconds

        def convert_to_time_object(seconds):
            """Function converts string to datetime.time object"""
            min, sec = divmod(seconds, 60)
            hour, min = divmod(min, 60)
            return datetime.time(hour, min, sec)

        # Establish completed status:
        if self.completed_status == "CMP":
            completed = True
        else:
            completed = False

        # Establish all required variables:
        active_status = self.yacht.is_active
        phrf_rating = self.yacht.phrf_rating
        time_correction_factor = 650 / (520 + phrf_rating)
        start_time = self.yacht_class_start
        finish_time = self.finish_time
        penalty = self.time_penalty

        # Establish start time based on yacht's class and event class start:
        if active_status and completed:

            # if yacht_class == "A" or "A1":
            #     start_time = self.event.start_A
            # elif yacht_class == "B":
            #     start_time = self.event.start_B
            # elif yacht_class == "C":
            #     start_time = self.event.start_C
            # elif yacht_class == "J":
            #     start_time = self.event.start_J

            # Convert all times to seconds:
            start = convert_to_seconds(start_time)
            finish = convert_to_seconds(finish_time)
            if self.time_penalty is not None:
                penalty = convert_to_seconds(self.time_penalty)
            else:
                penalty = 0

            # Calculate elapsed time and apply Time Correction Factor:
            elapsed_time = (finish - start) + penalty
            corrected_time = elapsed_time * time_correction_factor

            # Convert seconds into datetime.time object:
            corrected_time_obj = convert_to_time_object(corrected_time)

            # Return datetime.time object:
            return corrected_time_obj

        else:
            return None

    def save(self, *args, **kwargs):
        """override default save() method to capture posted_time by calling the calc_corrected_time @property/function"""
        self.posted_time = self.calc_corrected_time
        super(Result, self).save(*args, **kwargs)
