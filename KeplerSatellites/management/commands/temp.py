from django.core.management.base import BaseCommand

from keplersatellites.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        norad_id_list = range(1, 40667, 1)
        for norad_id in norad_id_list:
            Satellite.objects.update_or_create(norad_id=norad_id)
            print norad_id
