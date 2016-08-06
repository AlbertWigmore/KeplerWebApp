# import httplib
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
import json
import requests
from datetime import datetime
import time


class Query:
    def __init__(self):
        self.url_base = "https://www.space-track.org/"
        self.url_login = "ajaxauth/login"
        self.url_logout = "ajaxauth/logout"
        self.url_request = "basicspacedata/query/class/satcat/NORAD_CAT_ID/"
        self.url_request_tle = "https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/"
        self.url_request_box_score = "https://www.space-track.org/basicspacedata/query/class/boxscore/"
        self.url_request_postfix = "/metadata/false"
        self.url_request_postfix_tle = "/orderby/EPOCH%20desc/limit/1/metadata/false/distinct/true"
        self.cookie = None
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.credentials = {'identity': "albertwigmore@live.co.uk", 'password': "ucUuGCJLZq2xa4t"}
        self.data_acquired = 0
        self.max_data_rate = 6250 * 0.9  # 50kbps times a multiplier for headers
        self.time_initial = datetime.now()

    def login(self):
        url = self.url_base + self.url_login
        r = requests.post(url, data=self.credentials)
        if r.status_code == requests.codes.ok:
            self.cookie = r.cookies.get_dict()
            return self.cookie
        else:
            print("error:", "login", r.text)

    def logout(self):
        url = self.url_base + self.url_logout
        r = requests.get(url, cookies=self.cookie)
        if r.text == '"Successfully logged out"':
            return True
        return False

    def query(self, norad_id, request):
        if request == "satcat":
            url = self.url_base + self.url_request + str(norad_id) + self.url_request_postfix
        elif request == "tle":
            url = self.url_base + self.url_request_tle + str(norad_id) + self.url_request_postfix_tle
        elif request == "boxscore":
            url = self.url_request_box_score
        else:
            return None
        r = requests.get(url, headers=self.headers, cookies=self.cookie)

        print r.status_code

        if r.status_code == 401:
            url_cookie = self.url_base + self.url_login
            r = requests.post(url_cookie, data=self.credentials)
            if r.status_code == requests.codes.ok:
                self.cookie = r.cookies.get_dict()
            else:
                print("error:", "login", r.text)
            r = requests.get(url, headers=self.headers, cookies=self.cookie)

        self.data_acquired += len(r.text)

        if (self.data_acquired / ((datetime.now() - self.time_initial).total_seconds())) > self.max_data_rate:
            time.sleep(int((self.data_acquired / self.max_data_rate) -
                       (datetime.now() - self.time_initial).total_seconds()))

        try:
            json_dict = json.loads(r.text)
        except ValueError as json_error:
            json_dict = None
            print json_error

        return json_dict

'''
if __name__ == '__main__':
    c = Query()
    c.open()
    tle = c.query(50, "tle")
    tle = c.query(51, "tle")
    tle = c.query(52, "tle")
    c.close()
'''
'''
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
'''
