import random
import factory
from factory.django import DjangoModelFactory
from medspa.factories import MedSpaFactory
from service.factories import ServiceFactory
from .models import Appointment, StatusChoices


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment

    medspa = factory.SubFactory(MedSpaFactory)
    start_time = factory.Faker("future_datetime", end_date="+30d")
    status = factory.Faker(
        "random_element", elements=[choice[0] for choice in StatusChoices.choices]
    )

    @factory.post_generation
    def services(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for service in extracted:
                self.services.add(service)
        else:
            self.services.add(ServiceFactory(medspa=self.medspa))
