from django.shortcuts import render
from django.http import HttpResponse
from models import Country
from models import Satellite
from models import OrbitalElements
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist


def satellite_id(request, id):
    satellite = Satellite.objects.values().get(norad_id=id)
    return HttpResponse(json.dumps(satellite, cls=DjangoJSONEncoder))

def orbital_elements(request, id):
    orbitalelements = []
    orbitalelements.append(OrbitalElements.objects.filter(satellite_id=id).values())
    return HttpResponse(orbitalelements)

def country_name(request, name_id):
    return HttpResponse(json.dumps(Country.objects.values().get(name_id=name_id), cls=DjangoJSONEncoder))
