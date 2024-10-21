from django.db import models
from django.core.validators import RegexValidator


class MedSpa(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    email_address = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Med Spa"
        verbose_name_plural = "Med Spas"
