import pytest
from sbyra_src.racing.models import Yacht

""" 
Specifications: 

1. Test that a Yacht created with no phrf_rating and yacht_class values has is_active == False
2. Test that a Yacht created with phrf_rating value but has a yacht_class has is_active == False
3. Test that a Yacht created with phrf_rating and yacht_class has is_active == True
4. Test that a Yacht created with no phrf_rating or yacht_class can be updated with both and is_active == True
5. Test that slug takes name as input 

"""

yacht_data = [(1, "Yacht1"), (2, "Yacht2"), (3, "Yacht3")]


@pytest.mark.django_db
def test_load_fixture(load_db_fixtures):
    """Test that fixtures are loading. Only tests if at least one has been loaded."""
    data = len(Yacht.objects.all())
    assert data >= 1


@pytest.mark.django_db
@pytest.mark.parametrize("id, name", yacht_data)
class TestYachtModel:
    def test_yacht_data(self, id, name):
        """Test basic data entry into the model fields"""
        yacht = Yacht.objects.get(id=id)
        assert yacht.id == id
        assert yacht.name == name

    @pytest.mark.xfail
    def test_name_unique(self, id, name):
        """test that yacht name is unique"""
        pass
