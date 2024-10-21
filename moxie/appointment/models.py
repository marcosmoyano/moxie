from django.db import models
from django.db.models import Sum
from django.utils import timezone


class StatusChoices(models.TextChoices):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class Appointment(models.Model):
    medspa = models.ForeignKey("medspa.MedSpa", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    services = models.ManyToManyField("service.Service", related_name="appointments")
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.SCHEDULED
    )

    FINAL_STATUSES = (StatusChoices.CANCELED, StatusChoices.COMPLETED)

    @property
    def total_duration(self):
        return (
            self.services.aggregate(total=Sum("duration"))["total"]
            or timezone.timedelta()
        )

    @property
    def total_price(self):
        return self.services.aggregate(total=Sum("price"))["total"] or 0.00

    def __str__(self):
        return f"Appointment on {self.start_time}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
