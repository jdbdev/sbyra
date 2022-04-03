import datetime

import pytest
from django.db import IntegrityError
from django.utils.text import slugify
from sbyra_src.racing.models import Event, Result, Series, Yacht

""" 
Specifications: 

1. Test that a Yacht created with no phrf_rating and yacht_class values has is_active == False
2. Test that a Yacht created with phrf_rating value but has a yacht_class has is_active == False
3. Test that a Yacht created with phrf_rating and yacht_class has is_active == True
4. Test that a Yacht created with no phrf_rating or yacht_class can be updated with both and is_active == True
5. Test that slug takes name as input 

"""
yachtclub_data = []

yacht_data = [
    (1, "Yacht1", "A", "2022-02-02 22:02:02"),
    (2, "Yacht2", "A1", "2022-02-02 22:02:02"),
    (3, "Yacht3", "B", "2022-02-02 22:02:02"),
]

event_data = [()]

series_test_data = [
    (1, "Series_1", 2021),
    (2, "Series_2", 2022),
    (3, "Series_3", 2022),
]

result_data = []


@pytest.mark.django_db
def test_load_fixture(load_db_fixtures):
    """Test that fixtures are loading. Only tests if at least one has been loaded."""
    Yacht_data = Yacht.objects.all()
    Series_data = Series.objects.all()

    assert len(Yacht_data) >= 1
    assert len(Series_data) >= 1


# ------------------- MODEL: YACHT ------------------- #


@pytest.mark.django_db
@pytest.mark.parametrize("id, name, yacht_class, created", yacht_data)
class TestYachtModel:
    def test_yacht_data(self, id, name, yacht_class, created):
        """Test basic data entry into the model fields"""
        yacht = Yacht.objects.get(id=id)
        assert yacht.id == id
        assert yacht.name == name
        assert yacht.phrf_rating == None
        assert yacht.yacht_class == yacht_class
        assert yacht.is_active == False
        assert (
            yacht.created.strftime("%Y-%m-%d %H:%M:%S") == created
        )  # format the data from the database to match parameters


@pytest.mark.django_db
def test_slug_signal():
    """
    Test validates that yacht.slug is derived from yacht.name field. Use name field from model and not parametrize
    value to ensure that signal functions at DB level. Test Calls slugify function to match signal procedure.
    """
    yacht = Yacht.objects.get(id=1)
    assert yacht.slug == slugify(yacht.name)


@pytest.mark.django_db
def test_is_active_signal():
    """
    Test validates that adding phrf_rating and yacht_class will call yacht_is_active signal and set is_active = True
    """
    yacht1 = Yacht.objects.get(id=1)
    print(yacht1.is_active)
    yacht1.yacht_class = "A"
    yacht1.phrf_rating = 1
    yacht1.save()
    print(yacht1.is_active)
    assert yacht1.is_active == True


@pytest.mark.django_db
def test_name_unique():
    """test unique integrity of Yacht.name field"""
    with pytest.raises(IntegrityError):
        new_yacht1 = Yacht.objects.create(name="NewYacht1")
        new_yacht1.save()
        new_yacht2 = Yacht.objects.create(name="NewYacht1")
        new_yacht2.save()


# ------------------- MODEL: SERIES ------------------- #


@pytest.mark.django_db
@pytest.mark.parametrize("id, name, year", series_test_data)
class TestSeriesModel:
    def test_series_data(self, id, name, year):
        """Test basic data entry into the model fields"""
        series_data = Series.objects.get(id=id)
        assert series_data.id == id
        assert series_data.name == name
        assert series_data.year == year

    def test_year_data_type(self, id, name, year):
        """test that the year is entered as an integer"""
        series_data = Series.objects.get(id=id)
        assert type(series_data.year) == type(1)
        print(type(series_data.year))

    def test_current_year(self, id, name, year):
        pass


@pytest.mark.django_db
def test_default_manager():
    """test custom manager and additional methods on Series object managers"""
    s1 = Series.objects.all()  # test class DefaultSeriesManager
    assert len(s1) == 3
    s2 = Series.objects.by_year(
        2021
    )  # test class DefaultSeriesManager method: by_year(x)
    assert len(s2) == 1


@pytest.mark.django_db
def test_current_year_manager():
    """test custom manager that returns a filter queryset"""
    pass


@pytest.mark.django_db
def test_name_unique():
    """test unique integrity of Series.name field"""
    with pytest.raises(IntegrityError):

        new_series_1 = Series.objects.create(
            name="new_series_1", year=2022
        )
        new_series_1.save()
        new_series_2 = Series.objects.create(
            name="new_series_1", year=2022
        )
        new_series_2.save()


# ------------------- MODEL: EVENT -------------------- #

# ------------------- MODEL: RESULT ------------------- #
