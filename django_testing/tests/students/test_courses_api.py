from rest_framework.test import APIClient
from django.urls import reverse
import pytest
import random
from students.models import Course
from model_bakery import baker
from students.serializers import CourseSerializer
import json


# Проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_1st_courses(client, course_factory):
    object = course_factory(_quantity=1)
    print('obj:', object)
    payload = CourseSerializer(object[0]).data
    print('payload:', payload)
    url = reverse('course-detail', args=[str(payload['id'])])
    print('url', url)
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == payload['name']


# Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_courses(client, course_factory):
    course_factory(_quantity=5)
    url = reverse("course-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


# Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id_courses(client, course_factory):
    object = course_factory(_quantity=10)
    id_list = []
    for item in object:
        payload = CourseSerializer(item).data
        print('payload:', payload['id'])
        id_list.append(payload['id'])

    id_random = random.choice(id_list)
    print(id_random)

    payload = {
        'id': id_random,
    }

    url = reverse("course-list")
    response_filter = client.get(url, payload, format='json')
    print('response_filter: ', response_filter.data)
    assert response_filter.status_code == 200


# Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_courses(client, course_factory):
    object = course_factory(_quantity=10)
    name_list = []
    for item in object:
        payload = CourseSerializer(item).data
        print('payload:', payload['name'])
        name_list.append(payload['name'])
    name_random = random.choice(name_list)
    print(name_random)

    payload = {
        'name': name_random,
    }

    url = reverse("course-list")
    response_filter = client.get(url, payload, format='json')
    print('response_filter: ', response_filter.data)
    assert response_filter.status_code == 200



# Тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    payload = {
        'name': 'Химия2',
        'student': 1
    }
    url = reverse("course-list")
    print('url', url)
    response = client.post(url, data=payload)
    assert response.status_code == 201
    assert response.data['name'] == 'Химия2'


# Тест успешного обновления курса
@pytest.mark.django_db
def test_patch_course(client, course_factory):
    object = course_factory()
    print('obj:', object)
    payload = CourseSerializer(object).data
    print('payload:', payload)
    url = reverse('course-detail', args=[str(payload['id'])])
    payload2 = {
        'id': payload['id'],
        'name': 'Math',
    }
    response = client.patch(url, payload2, format='json')
    print('response_name', response.data['name'])
    assert response.data['name'] == payload2['name']
    assert response.status_code == 200

# Тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    object = course_factory()
    print('obj:', object)
    payload = CourseSerializer(object).data
    print('payload:', payload)
    url = reverse('course-detail', args=[str(payload['id'])])
    # Проверяем наличие
    response = client.get(url)
    assert response.data['id'] == payload['id']
    # Проверяем удаление
    response = client.delete(url, payload, format='json')
    print('response', response)
    assert response.status_code == 204
