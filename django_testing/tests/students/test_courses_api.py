from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from students.models import Course
from model_bakery import baker
from students.serializers import CourseSerializer
import json


# Проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_1st_courses(client, course_factory):
    objects = course_factory(_quantity=5)
    print('obj:', objects)
    # Use a DRF ModelSerializer to give us JSON
    for object in objects:
        payload = CourseSerializer(object).data
        print('payload:', payload)
        url = reverse("course-list")
        response = client.post(url, payload, format='json')
        assert response.status_code == 201


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
    objs = course_factory(_quantity=10)
    objs = Course.objects.filter(id=1)
    print('obj:', objs)
    for object in objs:
        payload = CourseSerializer(object).data
        print('payload:', payload)
        url = reverse("course-list")
        response = client.post(url, payload, format='json')
        print('response', response.data)
        assert response.status_code == 201


# Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_courses(client, course_factory):
    objs = course_factory(_quantity=10)
    objs = Course.objects.filter(name='Math')
    print('obj:', objs)
    for object in objs:
        payload = CourseSerializer(object).data
        print('payload:', payload)
        url = reverse("course-list")
        response = client.post(url, payload, format='json')
        print('response', response.data)
        assert response.status_code == 201
    assert len(objs) == 0

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
    url = reverse("course-list")
    response = client.post(url, payload, format='json')
    response = response.json()
    name = response['name']
    print('name:', name)
    payload = {
        'id': 1,
        'name': 'Math',
    }
    # url = reverse('course-detail')
    url = reverse('course-list')
    url = url + str(payload['id'])
    response = client.patch(url, payload, format='json')
    print('response', response)
    assert response.status_code == 301


# Тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):

    object = course_factory()
    print('obj:', object)
    payload = CourseSerializer(object).data
    print('payload:', payload)
    url = reverse("course-list")
    response = client.post(url, payload, format='json')
    response = response.json()
    name = response['name']
    print('name:', name)
    payload = {
        'id': 1,
        'name': 'Math',
    }
    # url = reverse('course-detail')
    url = reverse('course-list')
    url = url + str(payload['id'])
    response = client.delete(url, payload, format='json')
    print('response', response)
    assert response.status_code == 301
