import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

"""
Validation for canadian postal codes or us zip codes. Strips string passed from model field and verifies length of entry.
Additional validation for pattern recognition of postal codes with interger(I) and letter(L) pattern:
LIL ILI  or in regex - L \dL \dL\d

Canadian postal codes cannot start with: W or Z
Canadian postal codes cannot contain: D F I O Q

Regex pattern for Canadian Postal Code: 
Strict regex pattern: [ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]
User Kind regex pattern: ???

"""


def validate_postal_code(postal_code):
    """Validation for Canadian and American postal/zip codes. Valid String must be length of 5 or 6."""

    strip_postal_code = postal_code.replace(" ", "")
    upper_postal = strip_postal_code.upper()
    postal_length = len(upper_postal)
    postal_regex = r"[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"

    # Canadian or American postal code or zip validation:
    if postal_length > 6 or postal_length < 5:
        raise ValidationError("Invalid postal or zip code")

    # Canadian postal code validation:
    elif postal_length == 6:
        match = re.search(postal_regex, upper_postal)
        if match == None:
            raise ValidationError(f"Invalid postal code: {postal_code}")

    # American ZIP code validation:
    elif postal_length == 5:
        pass


def validate_year(value):
    """
    Validates that a year entry has 4 integers. Format: 2022.

    1. Converts multiple digit int to a list of ints using digitize()
    2. Checks length of list to match expected length (4 digits based on Format: 2022)
    3. Checks that all digits are ints (!!!redundant since IntegerField validates for ints!!!)

    """

    def digitize(n: int):
        """Converts int to list of ints - requires converting passed argument (n) to a string since data type int is not iterable."""
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
