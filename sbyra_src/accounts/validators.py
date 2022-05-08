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
[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]

"""


def validate_postal_code(postal_code):
    """Validation for Canadian and American postal/zip codes. Valid String must be length of 5 or 6."""

    clean_postal_code = postal_code.replace(" ", "")
    upper_postal = clean_postal_code.upper()
    postal_length = len(upper_postal)

    if postal_length > 6 or postal_length < 5:
        raise ValidationError("Invalid postal or zip code")

    # regex pattern match for Canadian postal codes:
    elif postal_length == 6:
        postal_regex = re.compile(
            r"[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"
        )
    # regex pattern match for American ZIP codes:
    elif postal_length == 5:
        zip_regex = re.compile(r"[]")
