from urllib import response
from rest_framework import status
from store.models import Collection
from model_bakery import baker
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/api/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_401(self, create_collection):
        # AAA (Arrange, Act, Assert)

        # Arrange: prepare the system on our test (creating objects, put the database on an initial state , ....)

        # Act
        response = create_collection({'title':'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, create_collection):
        authenticate()

        response = create_collection({'title':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticate, create_collection):   
        authenticate(is_staff=True)

        response = create_collection({'titel':''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None # we can do mutible assertion only when the are a related assertion otherwise we run each assertion in a separate test function

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)  

        response = api_client.get(f'/api/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0,
        }
