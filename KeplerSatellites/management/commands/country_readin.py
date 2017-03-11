from django.core.management.base import BaseCommand
from KeplerSatellites.models import *
from query import Query


class Command(BaseCommand):
    def handle(self, *args, **options):
        query_object = Query()
        query_object.login()
        boxscore = query_object.query(None, "boxscore")
        query_object.logout()
        for j, x in enumerate(boxscore):
            country_dict = {
                k: x.get(v, None) for k, v in (
                    ('name', u'COUNTRY'),
                    ('name_id', u'SPADOC_CD'),
                    ('in_orbit_unassigned', u'ORBITAL_UNASSIGNED'),
                    ('in_orbit_rocket', u'ORBITAL_ROCKET_BODY_COUNT'),
                    ('in_orbit_payload', u'ORBITAL_PAYLOAD_COUNT'),
                    ('in_orbit_debris', u'ORBITAL_DEBRIS_COUNT'),
                    ('in_orbit_total', u'ORBITAL_TOTAL_COUNT'),
                    ('decayed_rocket', u'DECAYED_ROCKET_BODY_COUNT'),
                    ('decayed_payload', u'DECAYED_PAYLOAD_COUNT'),
                    ('decayed_debris', u'DECAYED_DEBRIS_COUNT'),
                    ('decayed_total', u'DECAYED_TOTAL_COUNT'),
                )
            }
            country_dict['total'] = int(
                float(country_dict['in_orbit_total']) +
                float(country_dict['decayed_total'])
            )

            try:
                Country.objects.update_or_create(
                    name=country_dict['name'],
                    defaults=country_dict
                )
            except Country.DoesNotExist:
                print(Country.DoesNotExist)
