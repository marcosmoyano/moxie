import pytest
from datetime import timedelta
from decimal import Decimal

from django.urls import reverse
from service.factories import ServiceFactory
from service.models import Service
from medspa.factories import MedSpaFactory


@pytest.mark.django_db
def test_create_service(client):
    medspa = MedSpaFactory()
    data = {
        "medspa_id": medspa.id,
        "name": "Service",
        "description": "Description",
        "price": "150.00",
        "duration": "00:30:00",
    }
    url = reverse("create-service")
    response = client.post(url, data=data)
    assert response.status_code == 201
    service = Service.objects.get(name="Service")
    assert service.price == Decimal("150")
    assert service.duration == timedelta(minutes=30)
    assert service.medspa == medspa


@pytest.mark.django_db
def test_list_medspa_services(client):
    medspa = MedSpaFactory()
    ServiceFactory.create_batch(3, medspa=medspa)
    url = reverse("list-services", kwargs={"medspa": medspa.id})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.django_db
def test_get_service(client):
    service = ServiceFactory()
    url = reverse("get-update-service", kwargs={"service_id": service.id})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == service.description
    assert data["name"] == service.name
    assert data["price"] == str(service.price)
    assert data["id"] == service.id


@pytest.mark.django_db
def test_update_service(client):
    service = ServiceFactory()
    url = reverse("get-update-service", kwargs={"service_id": service.id})
    data = {
        "name": "New Name",
        "price": "100.00",
        "duration": "00:32:00",
        "description": "New desc",
    }
    response = client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "New desc"
    assert data["name"] == "New Name"
    assert data["price"] == "100.00"
    assert data["id"] == service.id
    assert data["duration"] == "00:32:00"
