from django.http import Http404
from django.shortcuts import render

from .models import Event, Result, Series, Yacht, YachtClub


def racing_home(request):
    yachts = Yacht.objects.all()
    events = Event.objects.all()
    series = Series.objects.all()
    context = {
        "yachts": yachts,
        "events": events,
        "series": series,
    }
    return render(request, "racing/racing_home.html", context)


def list_yachts(request):
    """View lists all yacht profiles"""

    yachts = Yacht.objects.all()
    yachts_active = Yacht.active.all()

    template = "racing/list_yachts.html"
    context = {
        "yachts": yachts,
        "yachts_active": yachts_active,
    }

    return render(request, template, context)


def yacht_details(request, pk):
    "View shows yacht details using Yacht.slug"
    yacht = Yacht.objects.get(pk=pk)
    template = "racing/yacht_details.html"
    context = {"yacht": yacht}
    return render(request, template, context)


def list_results(request):
    """View lists all results"""
    pass
