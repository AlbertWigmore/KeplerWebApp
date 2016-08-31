import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Country
from models import OrbitalElements
from models import Satellite
from .forms import SearchForm


def home_page(request):
    return render_to_response('index.html')


def satellite_id_old(request, id):
    satellite = Satellite.objects.get(norad_id=id)
    satellite_value = Satellite.objects.values().get(norad_id=id)
    satellite_dict = json.dumps(satellite_value, cls=DjangoJSONEncoder)

    orbital_element = OrbitalElements.objects.values().get(satellite=satellite)
    '''
    context = {
        'norad_id': norad_id,
        'sat_name': sat_name,
        'type': type,
        'site_code': site_code,
        'launch': launch,
        'decay': decay,
        'rcs_value': rcs_value,
        'elset_class': elset_classifation,
        'int_des': international_designator,
        'launch_year': launch_year,
        'launch_num': launch_num,
        'launch_piece': launch_piece,
        'originator': originator,
        'country': country,

        'period': period,
        'inclination': inclination,
        'apogee': apogee,
        'perigee': perigee,
        'RAAN': RAAN,
        'eccentricity': eccentricity,
        'argue_of_per': arguement_of_perigee,
        'object_type': object_type,
        'mean_anomly': mean_anomnoly,
        'mean_motion': mean_motion,
        'rev_epoch': rev_number_at_epoch,
        'first_der': first_derivative_of_mean_motion,
        'second_der': second_derivative_of_mean_motion,
        'b_drag_term': b_drag_term,
        'element_set_epoch': element_set_epoch,
        'epoch': epoch,
        'epoch_micro': epoch_microseconds,
        'tle1': tle_line_1,
        'tle2': tle_line_2,
    }
    '''

    return HttpResponse(orbital_element)


def country_name(request, name_id):
    info = Country.objects.filter(name_id__exact=name_id)
    data = {
        "country": info
    }

    return render_to_response('country.html', data, context_instance=RequestContext(request))


def country_count(request):
    info = Country.objects.values()
    data = {
        "country": info
    }

    return render_to_response('countries.html', data, context_instance=RequestContext(request))


def search_request(request, search):
    info = Satellite.objects.filter(sat_name__icontains=search).values('norad_id', 'sat_name', 'launch', 'decay',
                                                                       'country__name_id')
    data = {
        "satellite": info
    }

    return render_to_response('results.html', data, context_instance=RequestContext(request))


def satellite_id(request, id):
    # info = Satellite.objects.filter(norad_id__exact=id)
    satellite = Satellite.objects.get(norad_id=id)
    try:
        orb_info = OrbitalElements.objects.values().get(satellite=satellite)
    except:
        orb_info = {
            u'satellite_id': u'N/A',
            'mean_motion': u'N/A',
            'perigee': u'N/A',
            'RAAN': u'N/A',
            'second_derivative_of_mean_motion': u'N/A',
            'element_set_epoch': u'N/A',
            'object_type': u'N/A',
            'period': u'N/A',
            u'id': u'N/A',
            'mean_anomaly': u'N/A',
            'epoch': u'N/A',
            'b_drag_term': u'N/A',
            'tle_line_1': u'N/A',
            'argument_of_perigee': u'N/A',
            'tle_line_2': u'N/A',
            'eccentricity': u'N/A',
            'epoch_microsecond': u'N/A',
            'rev_number_at_epoch': u'N/A',
            'apogee': u'N/A',
            'first_derivative_of_mean_motion': u'N/A',
            'inclination': u'N/A'
        }

    data = {
        "satellite": satellite,
        "orbital": orb_info
    }

    return render_to_response('satellite.html', data, context_instance=RequestContext(request))


def sat_name(request):
    form = SearchForm(request.GET)
    print form

    return render(request, 'test2.html', {'form': form})


def search(request):
    satellite_list = Satellite.objects.all()
    if "sat_name" in request.GET:
        satellite_list = satellite_list.filter(sat_name__icontains=request.GET["sat_name"])
    paginator = Paginator(satellite_list, 25)

    page = request.GET.get('page')

    try:
        satellites = paginator.page(page)
    except PageNotAnInteger:
        satellites = paginator.page(1)
    except EmptyPage:
        satellites = paginator.page(paginator.num_pages)

    info = Satellite.objects.values('norad_id', 'sat_name', 'launch', 'decay', 'country__name_id')
    data = {
        "satellite": info
    }
    # return render_to_response('satellites.html', data, context_instance=RequestContext(request))
    return render(request, 'satellites.html', {'satellites': satellites})
