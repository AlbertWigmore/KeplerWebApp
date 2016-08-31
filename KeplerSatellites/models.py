from django.db import models


class OrbitalElements(models.Model):

    period = models.FloatField(blank=True, null=True)
    inclination = models.FloatField(blank=True, null=True)
    apogee = models.FloatField(blank=True, null=True)
    perigee = models.FloatField(blank=True, null=True)
    RAAN = models.FloatField(blank=True, null=True)
    eccentricity = models.FloatField(blank=True, null=True)
    argument_of_perigee = models.FloatField(blank=True, null=True)
    object_type = models.CharField(max_length=20, blank=True, null=True)
    mean_anomaly = models.FloatField(blank=True, null=True)
    mean_motion = models.FloatField(blank=True, null=True)
    rev_number_at_epoch = models.FloatField(blank=True, null=True)
    first_derivative_of_mean_motion = models.FloatField(blank=True, null=True)
    second_derivative_of_mean_motion = models.FloatField(blank=True, null=True)
    b_drag_term = models.FloatField(blank=True, null=True)
    element_set_epoch = models.FloatField(blank=True, null=True)
    epoch = models.DateTimeField(blank=True, null=True)
    epoch_microsecond = models.FloatField(blank=True, null=True)
    tle_line_1 = models.CharField(max_length=69, blank=True, null=True)
    tle_line_2 = models.CharField(max_length=69, blank=True, null=True)

    satellite = models.ForeignKey("Satellite", blank=True, null=True)


class Country(models.Model):


    name_id = models.CharField(max_length=4, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    in_orbit_unassigned = models.IntegerField(blank=True, null=True)
    in_orbit_payload = models.IntegerField(blank=True, null=True)
    in_orbit_rocket = models.IntegerField(blank=True, null=True)
    in_orbit_debris = models.IntegerField(blank=True, null=True)
    in_orbit_total = models.IntegerField(blank=True, null=True)
    decayed_payload = models.IntegerField(blank=True, null=True)
    decayed_rocket = models.IntegerField(blank=True, null=True)
    decayed_debris = models.IntegerField(blank=True, null=True)
    decayed_total = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)


class Satellite(models.Model):

    norad_id = models.IntegerField(blank=True, primary_key=True)
    sat_name = models.CharField(max_length=24, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    site_code = models.CharField(max_length=5, blank=True, null=True)
    launch = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    site = models.TextField(blank=True, null=True)
    decay = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rcs_value = models.CharField(max_length=7, blank=True, null=True)
    rcs_size = models.CharField(max_length=7, blank=True, null=True)
    elset_classification = models.CharField(max_length=1, blank=True, null=True)
    international_designator = models.CharField(max_length=12, blank=True, null=True)
    launch_year = models.IntegerField(blank=True, null=True)
    launch_num = models.IntegerField(blank=True, null=True)
    launch_piece = models.CharField(max_length=2, blank=True, null=True)
    current = models.CharField(max_length=2, blank=True, null=True)
    comment = models.CharField(max_length=80, blank=True, null=True)
    originator = models.CharField(max_length=20, blank=True, null=True)
    failed = models.BooleanField(default=True)

    country = models.ForeignKey("Country", blank=True, null=True)


class LastCheck(models.Model):
    time = models.DateTimeField(blank=True, null=True)