from rest_framework import generics
from .models import Service
from .serializers import (
    CreateServiceSerializer,
    ServiceSerializer,
    UpdateServiceSerializer,
)


class ListServiceAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(medspa_id=self.kwargs["medspa"])


class CreateServiceAPIView(generics.CreateAPIView):
    serializer_class = CreateServiceSerializer


class RetrieveUpdateServiceAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ServiceSerializer
    update_serializer_class = UpdateServiceSerializer
    lookup_url_kwarg = "service_id"

    def get_queryset(self):
        return Service.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        return self.update_serializer_class
