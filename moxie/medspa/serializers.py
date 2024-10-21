from rest_framework import serializers
from .models import MedSpa


class MedSpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedSpa
        fields = ["id", "name", "address", "phone_number", "email_address"]
