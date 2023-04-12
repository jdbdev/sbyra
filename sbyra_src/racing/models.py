# Pythom Module Imports:
import datetime

# Django Module Imports:
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Project level imports:
from sbyra_src.racing.choices import (
    CompletionStatusChoice,
    SpinnakerClassChoice,
    YachtClassChoice,
)
from sbyra_src.racing.managers import (
    ActiveYachtManager,
    CurrentYearSeriesManager,
    DefaultSeriesManager,
    DefaultYachtManager,
)

# Custom project level utility functions and validators:
from sbyra_src.utils.model_validators import (
    validate_postal_code,
    validate_year,
)
from sbyra_src.utils.time_conversions import (
    convert_to_seconds,
    convert_to_time_object,
)

User = settings.AUTH_USER_MODEL


""" 
All models related to yacht racing, including yachts, yacht clubs, events and results. This file contains only models.Model classes. 
Refer to separate files for;

managers.py (all models.Manager classes and custom methods)
signals.py (all receiver functions and signals)
choices.py (all related models.TextChoices classes for choice fields)
sbyra_src.utils (project level utility functions and validators)

- Models to remain explicit and include help_text.
- Do not include null=True in CharField unless unique=True and blank=True are set together
- Do not include null=True in EmailField, CharField, SlugField
- Keep model methods minimal and use other modules for additional functionality when possible
- Use on_delete=SET_NULL to preserve data entries
- Stay DRY and Keep common attributes and functionality in RacingCommon abstract model class.

"""


class RacingCommon(models.Model):
    """Abstract class for attributes and methods to be used by all other models"""

    created = models.DateTimeField(
        auto_now_add=True, null=True
    )  # null=True temporary only for testing
    updated = models.DateTimeField(
        auto_now=True, null=True
    )  # null=True temporary only for testing
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    # Soft delete and restore functionality *temporary solution needs review*
    def soft_delete(self):
        """allows a soft delete of data entries with restore capabilities"""
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class YachtClub(RacingCommon):
    """Yacht Club information - not required for racing functionality"""

    yacht_club_name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        help_text=_("enter yacht club name"),
    )
    slug = models.SlugField(
        blank=True,
        help_text=_("web safe url"),
    )
    city = models.CharField(
        max_length=100, blank=True, help_text=_("city or town of club")
    )
    street_name = models.CharField(
        max_length=100, blank=True, help_text=_("street of club")
    )
    street_number = models.CharField(
        max_length=10, blank=True, help_text=_("street number")
    )
    postal_code = models.CharField(
        _("postal code"),
        max_length=7,
        blank=True,
        help_text=_("format: A1AA1A"),
        validators=[validate_postal_code],
    )
    contact_first_name = models.CharField(
        max_length=100, blank=True, help_text=_("contact first name")
    )
    contact_last_name = models.CharField(
        max_length=100, blank=True, help_text=_("contact last name")
    )
    email = models.EmailField(
        _("email address"),
        max_length=100,
        blank=True,
        help_text=_("contact's email"),
    )

    class Meta:
        verbose_name = _("yacht club")
        verbose_name_plural = _("yacht clubs")

    def __str__(self):
        return self.yacht_club_name


class Spinnaker(RacingCommon):
    """Spinnaker class with adjustment value used in Result table to calculate corrected time"""

    spinnaker_class_name = models.CharField(
        max_length=3,
        choices=SpinnakerClassChoice.choices,
        blank=False,
        help_text=_("example: S1"),
        verbose_name="spinnaker class",
    )
    adjustment_value = models.IntegerField(
        max_length=3,
        help_text=_("phrf correction value based on spinnaker class"),
        verbose_name="spinnaker class adjustment",
    )

    class Meta:
        ordering = ["spinnaker_class_name"]
        verbose_name_plural = "spinnaker"

    def __str__(self):
        return self.spinnaker_class_name


class Yacht(RacingCommon):
    """Yacht class describing all attributes of an individual yacht"""

    yacht_name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        help_text=_("yacht name"),
    )
    slug = models.SlugField(
        blank=True,
        help_text=_("web safe url"),
        verbose_name="Web safe URL",
    )
    skipper = models.ForeignKey(
        User,  # Many-to-one relationship
        blank=True,
        null=True,
        related_name="yachts",  # User.yachts.all()
        help_text=_("yacht skipper"),
        verbose_name="skipper",
        on_delete=models.SET_NULL,  # skipper field will be set to null if a User is deleted
    )
    sail_num = models.CharField(
        max_length=25,
        blank=True,
        unique=True,
        help_text=_("Main sail number"),
        verbose_name="sail number",
    )
    yacht_type = models.CharField(
        max_length=50, blank=True, help_text=_("Type of yacht")
    )
    yacht_class = models.CharField(
        max_length=2,
        choices=YachtClassChoice.choices,
        blank=True,
        help_text=_("required to race"),
    )
    yacht_club = models.ForeignKey(
        YachtClub,  # Many-to-one relationship
        blank=True,
        null=True,
        related_name="yachts",  # YachtClub.yachts.all()
        on_delete=models.SET_NULL,
    )
    phrf_rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        help_text=_("required to race"),
    )
    spinnaker_class = models.ForeignKey(
        Spinnaker,  # Many-to-one relationship,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_("requires phrf rating and yacht class"),
    )

    objects = DefaultYachtManager()  # Yacht.objects.all()
    active = ActiveYachtManager()  # Yacht.active.all()

    class Meta:
        ordering = ["yacht_name"]
        verbose_name_plural = "yachts"

    def __str__(self):
        return self.yacht_name

    def get_absolute_url(self):
        # return f"/yachts/{self.slug}/"
        # pass to yacht-details url the keyword arguments - slug
        slug = self.slug
        return reverse("yacht-details", kwargs={"slug": slug})

    @property
    def spinnaker_adjust(self):
        """Returns an int value to be used in Result table calc_corrected_time property for phrf adjustment"""
        value = self.spinnaker_class.adjustment_value
        return int(value)


class Series(RacingCommon):
    """Series class describing all attributes of a series and linking sets of events"""

    name = models.CharField(
        max_length=100,
        blank=False,
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
        default=True,
        help_text=_(
            "archived if not current year"
        ),  # needs celevery script for periodic status check
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


class Event(RacingCommon):
    """Event class describing all attributes of an event. Start times based on Yacht class field"""

    event_date = models.DateField(blank=True)
    series = models.ForeignKey(
        Series, related_name="events", on_delete=models.CASCADE
    )  # Series.events.all()
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
        help_text="Add general event comments",
    )
    yachts = models.ManyToManyField(Yacht, through="Result")

    class Meta:
        ordering = ["event_date"]
        verbose_name_plural = "events"

    def __str__(self):
        return str(self.event_date)


class Result(RacingCommon):
    """Custom Through table linking Many to Many relationship between Yacht and Event"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    completed_status = models.CharField(
        max_length=3,
        choices=CompletionStatusChoice.choices,
        default=CompletionStatusChoice.CMP,
        help_text=_("race completion status"),
    )
    finish_time = models.TimeField(
        blank=True, null=True, help_text=_("Format: HH:MM:SS")
    )
    order_over_line = models.IntegerField(
        blank=True, null=True, help_text=_("enter sequence number")
    )
    time_penalty = models.TimeField(
        blank=True, null=True, help_text=_("Format: HH:MM:SS")
    )
    posted_time = models.TimeField(
        blank=True,
        null=True,
        help_text=_("Format: HH:MM:SS"),
    )
    used_spinnaker = models.BooleanField(
        default=False, help_text=_("spinnaker used during event")
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
        """
        Returns racing class start time for a specific yacht in a specific event based on yacht racing class.
        Called by calc_corrected_time property/method. Class start times are in Event model.

        """
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
        Returns the yacht's corrected time based on its elapsed time and time correction factors (phrf rating, penalties, etc.).
        Returns result only for active yachts that have completed the event. Returns None for all other yachts.

        *sbyra time correction factor used: 650/(520 + phrf_rating)*

        Corrected Time Algorithm:

        1. Establish start time based on yach's racing class and event's corresponding start time
        2. Convert start time and finish time to seconds for processing
        3. Calculate elapsed time in seconds between start time and finish time
        4. Apply time correction factor based on phrf_rating and yacht club's formula (may vary)
        5. Convert corrected time above (seconds) into datetime.time object for model TimeField()
        6. Save final datetime.time object into Result.posted_time

        Method called by save() to enter corrected time in posted_time field

        """

        # Establish completed status:
        if self.completed_status == "CMP":
            completed = True
        else:
            completed = False

        # Establish all other inputs:
        active_status = self.yacht.is_active
        used_spinnaker = self.used_spinnaker
        # Additional phrf adjustment based on spinnaker use and yacht's spinnaker class:
        if used_spinnaker:
            phrf_rating = int(
                (self.yacht.phrf_rating) - (self.yacht.spinnaker_adjust)
            )
        else:
            phrf_rating = int(self.yacht.phrf_rating)
        time_correction_factor = 650 / (520 + phrf_rating)
        start_time = self.yacht_class_start
        finish_time = self.finish_time
        penalty = self.time_penalty

        if active_status and completed:

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
