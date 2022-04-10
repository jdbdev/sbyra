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

    all_yachts = Yacht.objects.all()
    active_yachts = Yacht.active.all()

    template = "racing/list_yachts.html"
    context = {
        "all_yachts": all_yachts,
        "active_yachts": active_yachts,
    }

    return render(request, template, context)


def yacht_details(request, slug):
    "View shows yacht details using Yacht.slug"
    yacht = Yacht.objects.get(slug=slug)
    template = "racing/yacht_details.html"
    context = {"yacht": yacht}
    return render(request, template, context)


def list_results(request):
    """View lists all results"""
    pass
