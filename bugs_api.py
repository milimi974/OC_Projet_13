#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import requests
import urllib
from ftplib import FTP
import json

class BugsApi:

    def __init__(self, json_url, ftp_hostname="localhost", ftp_login=None, ftp_password=None, ftp_port=21):
        """
        this are the constructor
        :param json_url: string
        :param ftp_hostname: string
        :param ftp_login: string
        :param ftp_password: string
        :param ftp_port: int
        """
        self.json_url = json_url
        self.host = ftp_hostname
        self.port = ftp_port
        self.login = ftp_login
        self.password = ftp_password


    # this method return a ftp connexion
    def GetFtpSession(self):
        ftp = FTP()
        ftp.connect(self.host, self.port)
        ftp.login(self.login, self.password)
        return ftp

    # this method return a list of event date
    def GetCalendar(self):
        response = requests.get(self.json_url)
        return json.loads(response.text)


    # this save file on ftp
    def SaveOnline(self, filename, path='./', ftp_subpath=""):
        session = self.GetFtpSession()
        try:

            file = open("{}{}".format(path,filename), 'rb')  # file to send
            session.cwd(ftp_subpath)
            response = session.storbinary('STOR {}'.format(filename), file)  # send the file
            file.close()  # close file and FTP
            session.quit()
            return True
        except:
            return False

    # return list of file on ftp
    def GetFtpMeshList(self, ftp_subpath=""):
        session = self.GetFtpSession()
        session.cwd(ftp_subpath)
        files = []
        try:
            files = session.nlst()
        except:
            print("No files in this directory")
        session.quit()
        files.sort()
        return files

    # this method download mesh from online ftp
    def DownloadMesh(self, filename, ftp_subpath=""):
        session = self.GetFtpSession()
        session.cwd(ftp_subpath)
        directory = "./bugsmesh"
        file = os.path.join(directory, "bugs.blend")
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.isfile(file):
            os.remove(file)

        try:
            session.retrbinary('RETR %s' % filename, open(file, "wb").write)
            session.close
            return True
        except:
            session.close
            return False

