import httplib
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import json

def spacetrack_query(query):

    base = "www.space-track.org"
    auth = "/ajaxauth/login"

    json_query = {'identity': settings.USERNAME, 'password': settings.PASSWORD, 'query': query}
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

    conn = httplib.HTTPSConnection(base)
    conn.request("POST", auth, json.dumps(json_query, cls=DjangoJSONEncoder), headers)

    try:
        response = conn.getresponse()
        json_response = response.read()
    except:
        json_response = None

    try:
        json_dict = json.loads(json_response)
    except ValueError as json_error:
        json_dict = None
        print json_error

    conn.close()

    return json_dict
