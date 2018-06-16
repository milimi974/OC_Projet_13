#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import requests
import urllib
from ftplib import FTP
import json

class BugsApi:

    def __init__(self, json_url, ftp_hostname=None, ftp_login=None, ftp_password=None):
        """
        this are the constructor
        :param json_url: string
        :param ftp_hostname: string
        :param ftp_login: string
        :param ftp_password: string
        """
        self.json_url = json_url
        self.ftp_hostname = ftp_hostname
        self.ftp_login = ftp_login
        self.ftp_password = ftp_password

    # this method return a list of event date
    def GetCalendar(self):
        response = requests.get(self.json_url)
        return json.loads(response.text)

    # this save file on ftp
    def SaveOnline(self, file):
        session = FTP(self.ftp_hostname, self.ftp_login, self.ftp_password)
        file = open('kitten.jpg', 'rb')  # file to send
        session.storbinary('STOR kitten.jpg', file)  # send the file
        file.close()  # close file and FTP
        session.quit()

    # return list of file on ftp
    def GetFtpMeshList(self):
        session = FTP(self.ftp_hostname, self.ftp_login, self.ftp_password)
        files = []
        try:
            files = session.nlst()
        except ValueError:
            print("No files in this directory")
        session.quit()
        return files

    # this method download mesh from online ftp
    def DownloadMesh(self, filename):
        urllib.urlretrieve(self.ftp_hostname, filename)

