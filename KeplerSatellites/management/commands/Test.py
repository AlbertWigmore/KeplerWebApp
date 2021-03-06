import time
from datetime import datetime

from django.core.management.base import BaseCommand

from KeplerSatellites.models import *
from query import spacetrack_query


class Command(BaseCommand):
    def handle(self, *args, **options):

        norad_id_list = []
        created = Satellite.objects.filter(failed=True).values()
        for x in created:
            norad_id_list.append(x["norad_id"])

        for norad_id in norad_id_list:

            site_dict = {
                'AFETR': "Air Force Eastern Test Range",
                'AFWTR': "Air Force Western Test Range",
                'CAS': "Pegasus launched from Canary Islands Air Space",
                'ERAS': "Pegasus launched from Eastern Range Air Space",
                'FRGUI': "French Guiana",
                'HGSTR': "Hamma Guira Space Track Range",
                'JSC': "Jiuquan Satellite Launch Center, China",
                'KODAK': "Kodiak Island, Alaska",
                'KSCUT': "Kagoshima Space Center University Of Tokyo",
                'KWAJ': "Kwajalein",
                'KYMTR': "Kapustin Yar Missile and Space Complex",
                'NSC': "Naro Space Center, South Korea",
                'OREN': "Orenburg, Russia",
                'PKMTR': "Plesetek Missile and Space Complex",
                'SADOL': "Submarine Launch from Barents Sea, Russia",
                'SEAL': "Sea Launch",
                'SEM': "Semnan, Iran",
                'SNMLP': "San Marco Launch Platform",
                'SRI': "Sirharikota",
                'SVOB': "Svobodny, Russia",
                'TNSTA': "Tanegashima Space Center",
                'TSC': "Taiyaun Space Center, China",
                'TTMTR': "Tyuratam Missile and Space Complex",
                'UNKN': "Unknown",
                'WLPIS': "Wallos Island",
                'WOMRA': "Woomera",
                'WRAS': "Pegasus launched from Western Range Air Space",
                'XSC': "Xichang Space Center, China",
                'YAVNE': "Yavne, Israel",
                'YUN': "Yunsong, DPRK",
                None: None,
            }
            satellite_cat = spacetrack_query(
                "https://www.space-track.org/basicspacedata/query/class/" +
                "satcat/NORAD_CAT_ID/" + str(norad_id) + "/metadata/false")
            satellite_tle = spacetrack_query(
                "https://www.space-track.org/basicspacedata/query/class/" +
                "tle/NORAD_CAT_ID/" + str(norad_id) +
                "/metadata/false/distinct/true")

            print("Data Requests Done")

            if satellite_cat is None or satellite_tle is None:
                Satellite.objects.update_or_create(
                    norad_id=norad_id, failed=True
                )
                print("Space-Track Returned None, 10 Secs Til Next Query")
                time.sleep(10)
                continue
            else:
                k = 0
                for x in satellite_cat:
                    if str(satellite_cat[k].get(u'CURRENT', None)) == 'Y':
                        if satellite_cat[k].get(u'DECAY', None) is None:
                            launch = None
                        else:
                            launch = datetime.strptime(
                                satellite_cat[k].get(u'DECAY'), "%Y-%m-%d"
                            )

                        if satellite_cat[k].get(u'LAUNCH', None) is None:
                            decay = None
                        else:
                            decay = datetime.strptime(
                                satellite_cat[k].get(u'LAUNCH', None),
                                "%Y-%m-%d"
                            )
                        if satellite_cat[k].get(u'COUNTRY', None) is None:
                            country = None
                        else:
                            country = Country.objects.filter(
                                name_id=satellite_cat[k].get(u'COUNTRY')
                            )
                        satellite_dict = {
                            'norad_id': (
                                satellite_cat[k].get(u'NORAD_CAT_ID', None)
                            ),
                            'sat_name': (
                                satellite_cat[k].get(u'SATNAME', None)
                            ),
                            'site_code': (
                                satellite_cat[k].get(u'SITE', None)
                            ),
                            'launch': launch,
                            'site': site_dict[(
                                satellite_cat[k].get(u'SITE', None)
                            )],
                            'decay': decay,
                            'rcs_value': (
                                satellite_cat[k].get(u'RCSVALUE', None)
                            ),
                            'rcs_size': (
                                satellite_cat[k].get(u'RCS_SIZE', None)
                            ),
                            'elset_classification': (
                                satellite_cat[k].get(u'CLASSIFICATION_TYPE',
                                                     None)
                            ),
                            'international_designator': (
                                satellite_cat[k].get(u'INTLDES', None)
                            ),
                            'launch_year': (
                                satellite_cat[k].get(u'LAUNCH_YEAR', None)
                            ),
                            'launch_num': (
                                satellite_cat[k].get(u'LAUNCH_NUM', None)
                            ),
                            'launch_piece': (
                                satellite_cat[k].get(u'LAUNCH_PIECE', None)
                            ),
                            'current': (
                                satellite_cat[k].get(u'CURRENT', None)
                            ),
                            'comment': (
                                satellite_cat[k].get(u'COMMENT', None)
                            ),
                            'originator': (
                                satellite_cat[k].get(u'ORIGINATOR', None)
                            ),
                            'failed': False,

                            'country': country[0],
                        }
                    else:
                        pass
                    k += 1

                try:
                    satellite_foreign_key = Satellite.objects.update_or_create(
                        norad_id=(satellite_cat[0].get(
                            u'NORAD_CAT_ID', None)), defaults=satellite_dict
                    )
                    print("Satellite " + str(norad_id) + " Created")
                except Satellite.DoesNotExist:
                    satellite_foreign_key = None
                    print(Satellite.DoesNotExist)

                bulk_data = []
                j = 0
                for x in satellite_tle:
                    bulk_data.append(OrbitalElements(
                        period=(satellite_tle[j].get(
                            u'PERIOD', None)
                        ),
                        inclination=(satellite_tle[j].get(
                            u'INCLINATION', None)
                        ),
                        apogee=(satellite_tle[j].get(
                            u'APOGEE', None)
                        ),
                        perigee=(satellite_tle[j].get(
                            u'PERIGEE', None)
                        ),
                        RAAN=(satellite_tle[j].get(
                            u'RA_OF_ASC_NODE', None)
                        ),
                        eccentricity=(satellite_tle[j].get(
                            u'ECCENTRICITY', None)
                        ),
                        argument_of_perigee=(satellite_tle[j].get(
                            u'ARG_OF_PERICENTER', None)
                        ),
                        object_type=(satellite_tle[j].get(
                            u'OBJECT_TYPE', None)
                        ),
                        mean_anomaly=(satellite_tle[j].get(
                            u'MEAN_ANOMALY', None)
                        ),
                        mean_motion=(satellite_tle[j].get(
                            u'MEAN_MOTION', None)
                        ),
                        rev_number_at_epoch=(satellite_tle[j].get(
                            u'REV_AT_EPOCH', None)
                        ),
                        first_derivative_of_mean_motion=(satellite_tle[j].get(
                            u'MEAN_MOTION_DOT', None)
                        ),
                        second_derivative_of_mean_motion=(satellite_tle[j].get(
                            u'MEAN_MOTION_DDOT', None)
                        ),
                        b_drag_term=(satellite_tle[j].get(
                            u'BSTAR', None)
                        ),
                        element_set_epoch=(satellite_tle[j].get(
                            u'ELEMENT_SET_NO', None)
                        ),
                        tle_line_1=(satellite_tle[j].get(
                            u'TLE_LINE1', None)
                        ),
                        tle_line_2=(satellite_tle[j].get(
                            u'TLE_LINE2', None)
                        ),
                        epoch=datetime.strptime(satellite_tle[j].get(
                            u'EPOCH', None), "%Y-%m-%d %H:%M:%S"
                        ),
                        epoch_microsecond=(satellite_tle[j].get(
                            u'EPOCH_MICROSECONDS', None)
                        ),
                        satellite=satellite_foreign_key[0],
                    ))
                    j += 1
                try:
                    OrbitalElements.objects.bulk_create(bulk_data)
                    print("Orbital Elements Created")
                except OrbitalElements.DoesNotExist:
                    print(OrbitalElements.DoesNotExist)
