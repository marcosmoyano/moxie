from django.contrib import admin

from .models import Service, ServiceType, Product, Supplier

admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Product)
admin.site.register(Supplier)
