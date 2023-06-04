from django import forms
from django.forms import ModelForm

from .models import Event, Result, Series, Spinnaker, Yacht, YachtClub


class YachtForm(ModelForm):
    """Registration and edit form for Yachts"""

    class Meta:
        model = Yacht
        fields = (
            "yacht_name",
            "skipper",
            "sail_num",
            "yacht_type",
            "yacht_class",
            "yacht_club",
            "phrf_rating",
            "spinnaker_class",
        )


class YachtClubForm(ModelForm):
    class Meta:
        model = YachtClub


class SeriesForm(ModelForm):
    class Meta:
        model = Series


class EventForm(ModelForm):
    class Meta:
        model = Event


class ResultForm(ModelForm):
    class Meta:
        model = Result


class SpinnakerForm(ModelForm):
    class Meta:
        model = Result
