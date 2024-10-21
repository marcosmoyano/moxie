from django.db import models
from django.core.validators import MinValueValidator
from enum import Enum


class ServiceCategories(models.TextChoices):
    INJECTABLES = "Injectables"
    PEELS = "Peels"
    FAT_DISOLVING = "Fat Disolving"
    SCLEROTHERAPY = "Sclerotherapy"
    THREADS = "Threads"
    WEIGHTLOSS = "Weightloss"
    IV_THERAPY = "IV Therapy"
    VITAMIN_INJECTION = "Vitamin Injection"
    PEPTIDE_THERAPY = "Peptyde Therapy"
    ULTRASOUND = "Ultrasound"
    FACIALS = "Facials"
    OTHER_NON_MEDICAL = "Other Non Medical"
    CONSULTATION = "Consultation"
    FOLLOW_UP = "Follow Up"
    OTHER = "Other"


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    # whatever else could be needed here.
    # If using PostgeSQL I'd use an ArrayField for this particular field
    # but since for time constrains I'm using sqlite which does not support
    # ArrayField so this will be a M2M field

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    # whatever else is needed for a Product

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    # Whatever else is needed for a supplier

    def __str__(self):
        return self.name


class Service(models.Model):
    medspa = models.ForeignKey("medspa.MedSpa", on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=ServiceCategories.choices)
    service_types = models.ManyToManyField(
        "service.ServiceType", related_name="services"
    )
    products = models.ManyToManyField("service.Product", related_name="services")
    suppliers = models.ManyToManyField("service.Supplier", related_name="services")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    duration = models.DurationField()

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
