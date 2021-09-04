import pytest
from rest_framework.test import APIClient
from model_bakery.baker import make


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return make('Course', **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return make('Student', **kwargs)

    return factory
