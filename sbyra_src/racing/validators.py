from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    """validates that a year entry has 4 integers. Format: 2022"""
    values = list(value)
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    length = len(values)
    for i in values:
        if not i in nums:
            raise ValidationError(
                _("Entry not valid. Use format: 2022")
            )
    if length < 4:
        raise ValidationError(_("Use format: 2022"))
