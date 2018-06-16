#! /usr/bin/env python3
# coding: utf-8
import sys, os



PLUGIN_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PLUGIN_PATH)
from settings import *
from bugs_api import BugsApi
import requests,  json
from ftplib import FTP

class TestAPI(object):

    # test is connection status 200
    def test_connection_status_200(self):
        response = requests.get(JSON_URL)
        assert response.status_code == 200

    # test if connection return a list from json file
    def test_connection_return_list_from_json_file(self):
        ba = BugsApi(JSON_URL)
        data = ba.GetCalendar()
        assert isinstance(data, list)

    # test connection ftp
    def test_connection_ftp(self):
        session = FTP(FTP_HOSTNAME, FTP_LOGIN , FTP_PASSWORD)
        assert session.retrlines('LIST') == '226 Transfer complete'