from datetime import datetime
from rest_framework import generics

from .models import Appointment
from .serializers import AppointmentSerializer, ChangeAppointmentStatusSerializer


class GetAppointmentAPIView(generics.RetrieveAPIView):
    serializer_class = AppointmentSerializer
    lookup_url_kwarg = "appointment_id"

    def get_queryset(self):
        return Appointment.objects.all()


class CreateAppointmentAPIView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["services"] = self.request.data.get("services", [])
        return context


class ListAppointmentAPIView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        start_date = self.request.query_params.get("start_date")
        if start_date:
            try:
                date_object = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                # log an error. For now do nothing
                pass
            else:
                queryset = queryset.filter(start_time__date=date_object)
        return queryset


class UpdateAppointmentStatusAPIView(generics.UpdateAPIView):
    serializer_class = ChangeAppointmentStatusSerializer
    lookup_url_kwarg = "appointment_id"

    def get_queryset(self):
        return Appointment.objects.all()
