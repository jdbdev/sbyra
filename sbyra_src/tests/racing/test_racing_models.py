import pytest
from django.db import IntegrityError
from django.utils.text import slugify
from sbyra_src.racing.models import Yacht

""" 
Specifications: 

1. Test that a Yacht created with no phrf_rating and yacht_class values has is_active == False
2. Test that a Yacht created with phrf_rating value but has a yacht_class has is_active == False
3. Test that a Yacht created with phrf_rating and yacht_class has is_active == True
4. Test that a Yacht created with no phrf_rating or yacht_class can be updated with both and is_active == True
5. Test that slug takes name as input 

"""

yacht_data = [
    (1, "Yacht1", "A"),
    (2, "Yacht2", "A1"),
    (3, "Yacht3", "B"),
]


@pytest.mark.django_db
def test_load_fixture(load_db_fixtures):
    """Test that fixtures are loading. Only tests if at least one has been loaded."""
    data = Yacht.objects.all()
    assert len(data) >= 1


@pytest.mark.django_db
@pytest.mark.parametrize("id, name, yacht_class", yacht_data)
class TestYachtModel:
    def test_yacht_data(self, id, name, yacht_class):
        """Test basic data entry into the model fields"""
        yacht = Yacht.objects.get(id=id)
        assert yacht.id == id
        assert yacht.name == name
        assert yacht.phrf_rating == None
        assert yacht.yacht_class == yacht_class
        assert yacht.is_active == False


@pytest.mark.django_db
def test_slug_signal():
    """
    Test validates that yacht.slug is derived from yacht.name field. Use name field from model and not parametrize
    value to ensure that signal functions at DB level. Calls slugify function to match signal procedure.
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


@pytest.mark.django_db()
# @pytest.mark.xfail
def test_name_unique():

    with pytest.raises(IntegrityError):
        new_yacht1 = Yacht.objects.create(name="NewYacht1")
        new_yacht1.save()
        new_yacht2 = Yacht.objects.create(name="NewYacht1")
        new_yacht2.save()
