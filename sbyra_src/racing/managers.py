from django.db import models

# ------------------- MODEL: Yacht ------------------- #


class ActiveYachtManager(models.Manager):
    """Custom Yacht object Manager that filters for active Yachts only with additional methods"""

    def get_queryset(self):  # Yacht.active.all()
        return super().get_queryset().filter(is_active=True)

    def by_class(self, x):  # Yacht.active.by_class('x')
        return self.filter(yacht_class=x)


class DefaultYachtManager(models.Manager):
    """Default Yacht object manager with additional methods"""

    def by_class(self, x):  # Yacht.objects.by_class('x')
        return self.filter(yacht_class=x)

    def active(self):  # Yacht.objects.active()
        return self.filter(is_active=True)


# ------------------- MODEL: Series ------------------- #


class DefaultSeriesManager(models.Manager):
    """Default Series.objects.all() manager with additional filtering by_year"""

    def by_year(self, x):  # series.objects.by_year(x)
        return self.filter(year=x)


class CurrentYearSeriesManager(models.Manager):
    """Series.current.all() object manager returns only current_year == True instances"""

    def get_queryset(self):  # Series.current.all()
        return super().get_queryset().filter(current_year=True)
