from django.contrib import admin
from models import Satellite, OrbitalElements, Country

# Register your models here.
admin.site.register(Satellite)
admin.site.register(OrbitalElements)
admin.site.register(Country)