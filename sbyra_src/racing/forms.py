from django import forms
from django.forms import ModelForm

from .models import Event, Result, Series, Yacht, YachtClub


class YachtForm(ModelForm):
    """Form to register a new yacht"""

    class Meta:
        model = Yacht
        fields = "__all__"

    class Meta:
        model = Yacht
        fields = (
            "name",
            "skipper",
            "sail_num",
            "yacht_type",
            "yacht_class",
            "phrf_rating",
        )


# class YachtRegisterForm(forms.Form):
#     name = forms.CharField(
#         label="Yacht Register", max_length=100, required=False
#     )
#     skipper = forms.IntegerField(label="Skipper", required=False)
#     bio = forms.CharField(
#         label="Yacht Bio",
#         max_length=500,
#         required=False,
#         widget=forms.Textarea,
#     )


# class YachtClubForm(ModelForm):
#     class Meta:
#         model = YachtClub


# class Series(ModelForm):
#     class Meta:
#         model = Series


# class Event(ModelForm):
#     class Meta:
#         model = Event


# class Result(ModelForm):
#     class Meta:
#         model = Result
