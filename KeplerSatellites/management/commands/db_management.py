import time
from datetime import datetime

from django.core.management.base import BaseCommand

from keplersatellites.models import *
from query import Query


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
        # Need to sift through and slowly add satellites
        # Add most recent orbital element

        # once reached end of satellites need to add more orbital element
        # data and retrieve updates

        # Need to check and add country data and check for updates
