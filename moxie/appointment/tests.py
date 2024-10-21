import pytest
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django.urls import reverse
from django.utils.dateparse import parse_duration
from service.factories import ServiceFactory
from service.models import Service
from medspa.factories import MedSpaFactory
from .factories import AppointmentFactory


@pytest.mark.django_db
def test_appointment_total_duration():
    services = ServiceFactory.create_batch(2)
    appointment = AppointmentFactory(services=services)

    expected_duration = sum(
        (service.duration for service in services), timezone.timedelta()
    )
    assert appointment.total_duration == expected_duration


@pytest.mark.django_db
def test_appointment_total_price():
    services = ServiceFactory.create_batch(2)
    appointment = AppointmentFactory(services=services)

    expected_price = sum(service.price for service in services)
    assert appointment.total_price == expected_price


@pytest.mark.django_db
def test_create_appointment(client):
    medspa = MedSpaFactory()
    services = ServiceFactory.create_batch(3, medspa=medspa)
    data = {
        "services": [service.id for service in services],
        "medspa_id": medspa.id,
        "start_time": "2024-10-21 19:00:00",
    }
    url = reverse("create-appointment")
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201
    data = response.json()
    assert data["medspa"]["id"] == medspa.id
    service_ids = [sv["id"] for sv in data["services"]]
    for service in services:
        assert service.id in service_ids
    assert data["status"] == "Scheduled"


@pytest.mark.django_db
def test_get_appointment(client):
    appointment = AppointmentFactory()
    url = reverse("get-appointment", kwargs={"appointment_id": appointment.id})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["medspa"]["id"] == appointment.medspa_id
    assert data["status"] == appointment.status
    assert data["total_price"] == str(
        sum([x.price for x in appointment.services.all()])
    )
    assert parse_duration(data["total_duration"]) == appointment.total_duration


@pytest.mark.django_db
def test_change_status_appointment(client):
    appointment = AppointmentFactory(status="Scheduled")
    url = reverse(
        "change-appointment-status", kwargs={"appointment_id": appointment.id}
    )
    response = client.patch(
        url, data={"status": "Completed"}, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Completed"


@pytest.mark.django_db
def test_list_appointments(client):
    start_at = timezone.now() + timedelta(days=1)
    AppointmentFactory.create_batch(3, status="Scheduled", start_time=start_at)
    url = reverse("list-appointments")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(url, query_params={"status": "Scheduled"})
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(url, query_params={"status": "Canceled"})
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get(
        url, query_params={"start_date": start_at.strftime("%Y-%m-%d")}
    )
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(url, query_params={"start_date": "2024-10-21"})
    assert response.status_code == 200
    assert len(response.json()) == 0
