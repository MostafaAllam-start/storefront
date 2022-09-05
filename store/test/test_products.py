import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Product
@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/api/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_return_403(self, create_product):

        response = create_product({
                'title' : 'testProduct',
                'description': 'test description',
                'unit_price': 2.44,
                'inventory': 3,
                'collection':4,
            })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_return_403(self, authenticate, create_product):
        authenticate()

        response = create_product({
                'title' : 'testProduct',
                'description': 'test description',
                'unit_price': 2.44,
                'inventory': 3,
                'collection':4,
            })

        response.status_code == status.HTTP_403_FORBIDDEN
    # @pytest.mark.skip
    def test_if_invalid_data_return_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product({
                'title' : '',
                'description': '',
                'unit_price': '',
                'inventory': '',
                'collection': '',
            })
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        assert response.data['description'] is not None
        assert response.data['unit_price'] is not None
        assert response.data['inventory'] is not None


@pytest.mark.django_db
class TestRetreiveProduct:
    def test_if_product_is_exist_return_200(self, api_client):
        product = baker.make(Product)

        response = api_client.get(f'/api/products/{product.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == product.title
        assert response.data['description'] == product.description
        assert response.data['unit_price'] == str(product.unit_price)
        assert response.data['inventory'] == product.inventory
        assert response.data['collection'] == product.collection


        