from django.shortcuts import render

from .models import Event, Series, Yacht


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
    context = {
        "yachts": yachts,
        "yachts_active": yachts_active,
    }
    return render(request, "racing/list_yachts.html", context)


def yacht_details(request):
    "View shows yacht details"
    pass


def list_results(request):
    """View lists all results"""
    pass
