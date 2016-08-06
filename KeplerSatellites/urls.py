"""KeplerWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from views import satellite_id
from views import country_name
from views import orbital_elements
from views import country_count
from views import search_request
from views import home_page
from views import sat_name

urlpatterns = [
    #url(r'^satellite/(?P<id>[0-9]*)/$', satellite_id),
    url(r'^home/', home_page),
    url(r'^sat-name/', sat_name),
    url(r'^country/(?P<name_id>.*)/$', country_name),
    url(r'^countries', country_count),
    url(r'^orbitalelements/(?P<id>.*)/$', orbital_elements),
    url(r'^sat/(?P<id>[0-9]*)/$', satellite_id),
    url(r'^search/(?P<search>.*)/$', sat_name),
]
