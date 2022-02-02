import pytest
from django.core.management import call_command


@pytest.fixture
def create_admin_user(django_user_model):  # django_user_model will access the user model in settings
    """return admin user"""
    return django_user_model.objects.create_superuser(username="admin", email="a@admin.com", password="password")


@pytest.fixture(scope="session")
def load_db_fixtures(django_db_setup, django_db_blocker):  # both arguments from pytest-django to access the DB
    """load DB data fixture"""
    with django_db_blocker.unblock():  # pytest command to unblock the DB for access during testing
        call_command("loaddata", "racing_fixtures.json")
