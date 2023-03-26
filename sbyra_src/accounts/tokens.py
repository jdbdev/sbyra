from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import (
    text_type,  # six provides utilities to deal with different text between python 2 and python 3
)

# change PASSWORD_RESET_TIMEOUT_DAYS in settings.py file. Default 7 days


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """new account activation token to be used for email verification"""

    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)
            + text_type(timestamp)
            + text_type(user.is_active)
        )


# account_activation_token contains the hash value of generated token to utilize elsewhere
account_activation_token = AccountActivationTokenGenerator()
