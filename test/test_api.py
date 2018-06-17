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
        ba = BugsApi(JSON_URL,FTP_HOSTNAME, FTP_LOGIN , FTP_PASSWORD)
        session = ba.GetFtpSession()
        assert session.retrlines('LIST') == '226 Transfer complete'

    # test upload file to ftp
    def test_upload_file_ftp(self):
        ba = BugsApi(JSON_URL, FTP_HOSTNAME, FTP_LOGIN, FTP_PASSWORD)
        localpath = os.path.join(PLUGIN_PATH, "test/file/")
        response = ba.SaveOnline("mesh1.blend",path=localpath, ftp_subpath="mesh")
        assert response == True
        response = ba.SaveOnline("mesh2.blend", path=localpath, ftp_subpath="mesh")
        assert response == True
        response = ba.SaveOnline("mesh3.blend", path=localpath, ftp_subpath="mesh")
        assert response == True
        response = ba.SaveOnline("mesh4.blend", path=localpath, ftp_subpath="mesh")
        assert response == True

    # test list file on ftp
    def test_list_file_ftp(self):
        ba = BugsApi(JSON_URL, FTP_HOSTNAME, FTP_LOGIN, FTP_PASSWORD)
        list = ba.GetFtpMeshList("mesh")
        assert list == ["mesh1.blend","mesh2.blend","mesh3.blend","mesh4.blend"]