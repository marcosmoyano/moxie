import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import MedSpa  # Replace 'your_app' with the actual name of your Django app

fake = Faker()


class MedSpaFactory(DjangoModelFactory):
    class Meta:
        model = MedSpa

    name = factory.Faker("company")
    address = factory.Faker("address")
    phone_number = factory.LazyFunction(lambda: f"+1{fake.numerify('#########')}")
    email_address = factory.Faker("email")
