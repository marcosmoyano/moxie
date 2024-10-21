from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from service.views import (
    CreateServiceAPIView,
    ListServiceAPIView,
    RetrieveUpdateServiceAPIView,
)
from appointment.views import (
    ListAppointmentAPIView,
    CreateAppointmentAPIView,
    UpdateAppointmentStatusAPIView,
    GetAppointmentAPIView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("<int:medspa>/services/", ListServiceAPIView.as_view(), name="list-services"),
    path("service/", CreateServiceAPIView.as_view(), name="create-service"),
    path(
        "services/<int:service_id>/",
        RetrieveUpdateServiceAPIView.as_view(),
        name="get-update-service",
    ),
    path("appointment/", CreateAppointmentAPIView.as_view(), name="create-appointment"),
    path(
        "appointments/<int:appointment_id>/",
        GetAppointmentAPIView.as_view(),
        name="get-appointment",
    ),
    path(
        "appointment/<int:appointment_id>/change-status/",
        UpdateAppointmentStatusAPIView.as_view(),
        name="change-appointment-status",
    ),
    path("appointments/", ListAppointmentAPIView.as_view(), name="list-appointments"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
