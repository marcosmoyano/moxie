from rest_framework import serializers
from service.models import Service
from service.serializers import ServiceSerializer
from medspa.models import MedSpa
from medspa.serializers import MedSpaSerializer
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    medspa = MedSpaSerializer(read_only=True)
    medspa_id = serializers.PrimaryKeyRelatedField(
        queryset=MedSpa.objects.all(), source="medspa", write_only=True
    )
    services = ServiceSerializer(many=True, read_only=True)
    total_duration = serializers.DurationField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "medspa",
            "medspa_id",
            "start_time",
            "services",
            "status",
            "total_duration",
            "total_price",
        ]
        extra_kwargs = {"status": {"required": False}}

    def create(self, validated_data):
        services_data = self.context.get("services", [])
        appointment = Appointment.objects.create(**validated_data)
        services = Service.objects.filter(id__in=services_data)
        appointment.services.add(*services)
        return appointment

    def update(self, instance, validated_data):
        services_data = self.context.get("services", [])
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        # Update services if services_data
        if services_data:
            instance.services.clear()
            services = Service.objects.filter(id__in=services_data)
            instance.services.add(*services)
        return instance


class ChangeAppointmentStatusSerializer(serializers.ModelSerializer):
    medspa = MedSpaSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "status",
            "medspa",
            "services",
            "start_time",
            "total_price",
            "total_duration",
        ]
        read_only_fields = [
            "medspa",
            "services",
            "start_time",
            "total_price",
            "total_duration",
        ]

    def validate_status(self, value):
        if value not in Appointment.FINAL_STATUSES:
            raise serializers.ValidationError(
                "Trying to change to a non-terminal status"
            )
        return value

    def validate(self, attrs):
        if self.instance.status in Appointment.FINAL_STATUSES:
            raise serializers.ValidationError(
                "Trying to change an appointment in a terminal status"
            )
        return super().validate(attrs)
