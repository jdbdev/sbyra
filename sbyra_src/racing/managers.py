from django.db import models

# ------------------- MODEL: YACHT ------------------- #


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


# ------------------- MODEL: EVENT ------------------- #

# ------------------- MODEL: RESULTS ------------------#
