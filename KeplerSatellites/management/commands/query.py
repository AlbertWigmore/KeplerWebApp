# import httplib
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
import json
import time
from datetime import datetime, timedelta

import requests


class Query:
    def __init__(self):
        self.url_base = "https://www.space-track.org/"
        self.url_login = "ajaxauth/login"
        self.url_logout = "ajaxauth/logout"
        self.url_request = "basicspacedata/query/class/satcat/NORAD_CAT_ID/"
        self.url_request_tle = "https://www.space-track.org/basicspacedata/" +\
                               "query/class/tle/NORAD_CAT_ID/"
        self.url_request_box_score = "https://www.space-track.org/" + \
                                     "basicspacedata/query/class/boxscore/"
        self.url_request_postfix = "/metadata/false"
        self.url_request_postfix_tle = "/orderby/EPOCH%20desc/limit/1/" + \
                                       "metadata/false/distinct/true"
        self.cookie = None
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json'}
        self.credentials = {'identity': "albertwigmore@live.co.uk",
                            'password': "ucUuGCJLZq2xa4t"}
        self.data_acquired = 0
        self.max_data_rate = 6250 * 0.9  # 50kbps times multiplier for headers
        self.time_initial = datetime.now()
        self.query_times = [datetime.now() - timedelta(minutes=1)] * 20

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
            url = self.url_base + self.url_request + str(norad_id) + \
                self.url_request_postfix
        elif request == "tle":
            url = self.url_base + self.url_request_tle + str(norad_id) + \
                self.url_request_postfix_tle
        elif request == "boxscore":
            url = self.url_request_box_score
        else:
            return None

        # 20 request per minute API throttling requirement
        sleep_time = 60 - (datetime.now() - self.query_times.pop(0)).\
            total_seconds()
        if sleep_time > 0:
            time.sleep(sleep_time)

        try:
            r = requests.get(url, headers=self.headers, cookies=self.cookie)
        finally:
            self.query_times.append(datetime.now())

        if r.status_code == 401:
            url_cookie = self.url_base + self.url_login
            r = requests.post(url_cookie, data=self.credentials)
            if r.status_code == requests.codes.ok:
                self.cookie = r.cookies.get_dict()
            else:
                print("error:", "login", r.text)
            r = requests.get(url, headers=self.headers, cookies=self.cookie)

        # Data rate of 50kbps requirement
        self.data_acquired += len(r.text)

        if (self.data_acquired / ((datetime.now() -
                                   self.time_initial).
                                  total_seconds())) > self.max_data_rate:

            time.sleep(int((self.data_acquired / self.max_data_rate) -
                           (datetime.now() - self.time_initial).
                           total_seconds()))

        if r.status_code != 200:
            print("headers: ", r.headers)
            print(r.text)
            raise IOError("Invalid Server Response, Status Code: %i" %
                          r.status_code)

        json_dict = json.loads(r.text)

        return json_dict
