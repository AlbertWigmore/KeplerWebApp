from django.core.management.base import BaseCommand
from datetime import datetime
import json
import httplib
from django.core.serializers.json import DjangoJSONEncoder
from KeplerSatellites.models import *
from django.conf import settings

class Command(BaseCommand):
    def country(self):
        pass

    def satellite(self):
        pass

    def handle(self, *args, **options):

        base = "www.space-track.org"
        auth = "/ajaxauth/login"
        satellite_query = "https://www.space-track.org/basicspacedata/" \
                          "query/class/tle/NORAD_CAT_ID/"
        test = "https://www.space-track.org/basicspacedata/query/class/satcat/orderby/NORAD_CAT_ID asc/" \
               "limit/1/metadata/false"

        # Returns tle data for norad id, used for orbital elements
        test2 = "https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/5/metadata/false/distinct/true"

        # Returns data from satcat for norad id, only used for launch data
        test3 = "https://www.space-track.org/basicspacedata/query/class/satcat/NORAD_CAT_ID/" \
               "5/metadata/false"

        country_query = "https://www.space-track.org/basicspacedata/query/class/boxscore/"
        jsonquery = {'identity': settings.username, 'password': settings.password, 'query': test3}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        conn = httplib.HTTPSConnection(base)
        conn.request("POST", auth, json.dumps(jsonquery, cls=DjangoJSONEncoder), headers)

        try:
            response = conn.getresponse()
            satellite_json = response.read()
            print satellite_json
        except:
            satellite_json = None

        conn.close()

        site_dict = {

        }

        try:
            satellite_cat = json.loads(satellite_json)

            j = 0
            for x in satellite_cat:
                satellite_dict = {
                    'norad_id': (satellite_cat[j].get(u'NORAD_CAT_ID', None)),
                    'sat_name': (satellite_cat[j].get(u'SATNAME', None)),

                    'site_code': (satellite_cat[j].get(u'SITE', None)),
                    'launch': (satellite_cat[j].get(u'LAUNCH', None)),
                    #'site': (satellite_cat[j].get(u'', None)),
                    'decay': (satellite_cat[j].get(u'DECAY', None)),
                    'object_type': (satellite_cat[j].get(u'OBJECT_TYPE', None)),
                    'rcs_value': (satellite_cat[j].get(u'RCSVALUE', None)),
                    'rcs_size': (satellite_cat[j].get(u'RCS_SIZE', None)),
                    #'elset_classification': (satellite_cat[j].get(u'', None)),
                    'international_designator': (satellite_cat[j].get(u'INTLDES', None)),

                    'launch_year': (satellite_cat[j].get(u'SITE', None)),
                    'launch_num': (satellite_cat[j].get(u'SITE', None)),
                    'launch_piece': (satellite_cat[j].get(u'SITE', None)),
                    'current': (satellite_cat[j].get(u'SITE', None)),
                    'comment': (satellite_cat[j].get(u'SITE', None)),
                    'originator': (satellite_cat[j].get(u'SITE', None)),

                    'country': (satellite_cat[j].get(u'COUNTRY', None)),
                }

                orbital_elements_dict = {
                    'period': (satellite_cat[j].get(u'PERIOD', None)),
                    'inclination': (satellite_cat[j].get(u'INCLINATION', None)),
                    'apogee': (satellite_cat[j].get(u'APOGEE', None)),
                    'perigee': (satellite_cat[j].get(u'PERIGEE', None)),
                    'RAAN': (satellite_cat[j].get(u'', None)),
                    'eccentricity': (satellite_cat[j].get(u'', None)),
                    'argument_of_perigee': (satellite_cat[j].get(u'', None)),
                    'mean_anomoly': (satellite_cat[j].get(u'', None)),
                    'mean_motion': (satellite_cat[j].get(u'', None)),
                    'rev_number_at_epoch': (satellite_cat[j].get(u'', None)),
                    'first_derivative_of_mean_motion': (satellite_cat[j].get(u'', None)),
                    'second_derivative_of_mean_motion': (satellite_cat[j].get(u'', None)),
                    'b_drag_term': (satellite_cat[j].get(u'', None)),
                    'element_set_epoch': (satellite_cat[j].get(u'', None)),
                    'tle_line_1': (satellite_cat[j].get(u'', None)),
                    'tle_line_2': (satellite_cat[j].get(u'', None)),
                }

        except ValueError as json_error:
            print json_error
