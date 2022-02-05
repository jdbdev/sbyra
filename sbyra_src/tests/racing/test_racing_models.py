import pytest
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

yacht_data = [(1, "Yacht1", "A"), (2, "Yacht2", "A1"), (3, "Yacht3", "B")]


@pytest.mark.django_db
def test_load_fixture(load_db_fixtures):
    """Test that fixtures are loading. Only tests if at least one has been loaded."""
    data = len(Yacht.objects.all())
    assert data >= 1


@pytest.mark.django_db
@pytest.mark.parametrize("id, name, yacht_class", yacht_data)
class TestYachtModel:
    def test_yacht_data(self, id, name, yacht_class):
        """Test basic data entry into the model fields"""
        yacht = Yacht.objects.get(id=id)
        print(yacht.yacht_class)
        assert yacht.id == id
        assert yacht.name == name
        assert yacht.yacht_class == yacht_class

    def test_slug_signal(self, id, name, yacht_class):
        """
        Test verifies that yacht.slug is derived from yacht.name field. Use name field from model and not parametrize
        value to ensure that signal functions at DB level. Calls slugify function to match signal procedure.
        """
        yacht = Yacht.objects.get(id=id)
        print(yacht.name)
        print(yacht.slug)
        assert yacht.slug == slugify(yacht.name)

    @pytest.mark.xfail
    def test_name_unique(self, id, name, yacht_class):
        """test that yacht name is unique"""
        pass
