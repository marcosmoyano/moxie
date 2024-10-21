from rest_framework import serializers
from medspa.models import MedSpa
from medspa.serializers import MedSpaSerializer
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    medspa = MedSpaSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "medspa",
            "name",
            "description",
            "price",
            "duration",
        ]


class CreateServiceSerializer(serializers.ModelSerializer):
    medspa = MedSpaSerializer(read_only=True)
    medspa_id = serializers.PrimaryKeyRelatedField(
        queryset=MedSpa.objects.all(), source="medspa", write_only=True
    )

    class Meta:
        model = Service
        fields = [
            "id",
            "medspa",
            "medspa_id",
            "name",
            "description",
            "price",
            "duration",
        ]


class UpdateServiceSerializer(serializers.ModelSerializer):
    medspa = MedSpaSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "medspa",
            "name",
            "description",
            "price",
            "duration",
        ]
