from django.forms import formset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import YachtForm
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


def yacht_register(request):
    if request.method == "POST":
        form = YachtForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            yacht = Yacht.objects.create(name=name)
            yacht.save()
            return HttpResponse(
                f"you have registered a Yacht named: {yacht.name}"
            )

    template = "racing/yacht_register.html"
    user_name = request.user
    skipper_id = request.user.id
    form = YachtForm(
        {"skipper": skipper_id}
    )  # name value will appear in form field widget
    context = {
        "form": form,
        "user_name": user_name,
    }
    return render(request, template, context)


def yacht_details(
    request, slug
):  # slug being passed to view by yacht-details url
    """View shows yacht details based on slug from URL pattern"""

    yacht = get_object_or_404(Yacht, slug=slug)
    template = "racing/yacht_details.html"
    context = {
        "yacht": yacht,
        "slug": slug,
    }
    return render(request, template, context)


def list_results(request):
    """View lists all results"""
    pass


"""
NOTES:

    get_object_or_404() replaces:

    try:
        yacht = Yacht.objects.get(slug=slug)
    Except Yacht.DoesNotExist:
        raise http404("Yacht does not exist")

    Form Binding:
    To bind a value to a form; 
        form = FormName({'name': 'Julien'})

"""
