from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    """
    Validates that a year entry has 4 integers. Format: 2022. Model field is IntegerField and needs to be
    converted to a list to verify length.

    1. Converts multiple digit int to a list of ints using digitize()
    2. Checks length of list to match expected length (4 digits based on Format: 2022)
    3. Checks that all digits are ints (!!!redundant since IntegerField validates for ints!!!)

    """

    def digitize(n):
        """Converts int to list of ints - requires converting n to a string since type int is not iterable."""
        return [int(d) for d in str(n)]

    # def digitize(n):
    #     return list(map(int, str(n)))

    values = digitize(value)
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    length = len(values)

    if length < 4:
        raise ValidationError(_("Entry not valid. Use format: 2022"))
    for i in values:
        if not i in nums:
            raise ValidationError(
                _("Entry not valid. Use format: 2022")
            )
