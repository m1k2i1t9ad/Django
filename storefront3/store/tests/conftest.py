from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User

######################################
#fixtures:powerfull feature in pytest used to remove duplication inthe test code:
@pytest.fixture #this decorator makes the function(method) below a fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def force_authentication(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))