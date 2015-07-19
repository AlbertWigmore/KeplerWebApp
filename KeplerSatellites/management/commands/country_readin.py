from django.core.management.base import BaseCommand
from datetime import datetime
import json
import httplib
from django.core.serializers.json import DjangoJSONEncoder
from KeplerSatellites.models import *
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):

        base = "www.space-track.org"
        auth = "/ajaxauth/login"
        satellite_query = "https://www.space-track.org/basicspacedata/" \
                 "query/class/tle/NORAD_CAT_ID/25544/orderby/EPOCH desc/" \
                 "limit/22/"
        country_query = "https://www.space-track.org/basicspacedata/query/class/boxscore/"
        jsonquery = {'identity': settings.username, 'password': settings.password, 'query': country_query}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        conn = httplib.HTTPSConnection(base)
        conn.request("POST", auth, json.dumps(jsonquery, cls=DjangoJSONEncoder), headers)

        try:
            response = conn.getresponse()
            boxscore_json = response.read()
        except:
            pass

        conn.close()
        boxscore = json.loads(boxscore_json)

        j = 0
        for x in boxscore:
            country_dict = {
                'name': (boxscore[j].get(u'COUNTRY', None)),
                'name_id': (boxscore[j].get(u'SPADOC_CD',None)),
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

            print country_dict

            try:
                Country.objects.update_or_create(name=(boxscore[j].get(u'COUNTRY', None)), defaults=country_dict)
            except Country.DoesNotExist:
                print Country.DoesNotExist
            j += 1

