from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import pytest

user = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=user(is_staff=is_staff))
    return do_authenticate
