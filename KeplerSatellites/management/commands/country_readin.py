from django.core.management.base import BaseCommand
# import json
# import httplib
# from django.core.serializers.json import DjangoJSONEncoder
from KeplerSatellites.models import *
# from django.conf import settings
# from query import spacetrack_query
from query import Query


class Command(BaseCommand):

    def handle(self, *args, **options):
        query_object = Query()
        query_object.login()
        boxscore = query_object.query(None, "boxscore")
        query_object.logout()
        j = 0
        for x in boxscore:
            country_dict = {
                'name': (boxscore[j].get(u'COUNTRY', None)),
                'name_id': (boxscore[j].get(u'SPADOC_CD', None)),
                'in_orbit_unassigned': (boxscore[j].get(u'ORBITAL_UNASSIGNED', None)),
                'in_orbit_rocket': (boxscore[j].get(u'ORBITAL_ROCKET_BODY_COUNT', None)),
                'in_orbit_payload': (boxscore[j].get(u'ORBITAL_PAYLOAD_COUNT', None)),
                'in_orbit_debris': (boxscore[j].get(u'ORBITAL_DEBRIS_COUNT', None)),
                'in_orbit_total': (boxscore[j].get(u'ORBITAL_TOTAL_COUNT', None)),
                'decayed_rocket': (boxscore[j].get(u'DECAYED_ROCKET_BODY_COUNT', None)),
                'decayed_payload': (boxscore[j].get(u'DECAYED_PAYLOAD_COUNT', None)),
                'decayed_debris': (boxscore[j].get(u'DECAYED_DEBRIS_COUNT', None)),
                'decayed_total': (boxscore[j].get(u'DECAYED_TOTAL_COUNT', None)),
                'total': int(float((boxscore[j].get(u'DECAYED_TOTAL_COUNT', None))) +
                             float((boxscore[j].get(u'ORBITAL_TOTAL_COUNT', None))))}

            try:
                Country.objects.update_or_create(name=(boxscore[j].get(u'COUNTRY', None)), defaults=country_dict)
            except Country.DoesNotExist:
                print Country.DoesNotExist
            j += 1
