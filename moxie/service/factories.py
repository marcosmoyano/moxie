import random
import factory
from factory.django import DjangoModelFactory
from datetime import timedelta
from medspa.factories import MedSpaFactory
from .models import ServiceCategories, ServiceType, Product, Supplier, Service


class ServiceTypeFactory(DjangoModelFactory):
    class Meta:
        model = ServiceType

    name = factory.Faker("word")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Faker("company")


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    medspa = factory.SubFactory(MedSpaFactory)
    category = factory.Faker("random_element", elements=ServiceCategories.values)
    name = factory.Faker("catch_phrase")
    description = factory.Faker("paragraph")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    duration = factory.LazyFunction(lambda: timedelta(minutes=random.randint(15, 180)))

    @factory.post_generation
    def service_types(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for service_type in extracted:
                self.service_types.add(service_type)
        else:
            self.service_types.add(ServiceTypeFactory())

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)
        else:
            self.products.add(ProductFactory())

    @factory.post_generation
    def suppliers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for supplier in extracted:
                self.suppliers.add(supplier)
        else:
            self.suppliers.add(SupplierFactory())
