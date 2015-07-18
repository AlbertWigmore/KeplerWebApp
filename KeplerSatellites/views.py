from django.shortcuts import render
from django.http import HttpResponse
from models import Country
from models import Satellite
from models import OrbitalElements
import json
from django.core.serializers.json import DjangoJSONEncoder


def satellite_id(request, id):
    satellite = Satellite.objects.values().get(pk=id)
    satellite["orbital_elements"] = OrbitalElements.objects.values().get(satellite=id)
    return HttpResponse(json.dumps(satellite, cls=DjangoJSONEncoder))


def country_name(request, name_id):
    return HttpResponse(json.dumps(Country.objects.values().get(name_id=name_id), cls=DjangoJSONEncoder))
