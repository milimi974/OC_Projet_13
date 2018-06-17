#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import requests
import urllib
from ftplib import FTP
import json
import tempfile


class BugsApi:

    def __init__(self, json_url, ftp_hostname="localhost", ftp_login=None, ftp_password=None, ftp_subpath="", ftp_port=21):
        """
        this are the constructor
        :param json_url: string
        :param ftp_hostname: string
        :param ftp_login: string
        :param ftp_password: string
        :param ftp_port: int
        :param ftp_port: int
        """
        self.json_url = json_url
        self.host = ftp_hostname
        self.port = ftp_port
        self.login = ftp_login
        self.password = ftp_password
        self.ftp_subpath = ftp_subpath


    # this method return a ftp connexion
    def GetFtpSession(self):
        ftp = FTP()
        ftp.connect(self.host, int(self.port))
        ftp.login(self.login, self.password)
        return ftp

    # this method return a list of event date
    def GetCalendar(self):
        response = requests.get(self.json_url)
        return json.loads(response.text)


    # this save file on ftp
    def SaveOnline(self, filename, direction=""):
        session = self.GetFtpSession()
        session.cwd(self.ftp_subpath)
        try:
            file = open(os.path.join(direction,filename), 'rb')  # file to send
            response = session.storbinary('STOR {}'.format(filename), file)  # send the file
            file.close()  # close file and FTP
            session.quit()
            return True
        except:
            return False

    # return list of file on ftp
    def GetFtpMeshList(self):
        session = self.GetFtpSession()
        session.cwd(self.ftp_subpath)
        files = []
        try:
            files = session.nlst()
        except:
            print("No files in this directory")
        session.quit()
        files.sort()
        return files

    # this method download mesh from online ftp
    def DownloadMesh(self, filename):
        session = self.GetFtpSession()
        session.cwd(self.ftp_subpath)
        directory = os.path.join(tempfile.gettempdir(), "bugsmesh")
        filename_split, file_extension = os.path.splitext(filename)

        if file_extension == ".blend":
            file = os.path.join(directory, "bugs.blend")
        elif file_extension == ".obj":
            file = os.path.join(directory, "bugs.obj")
        else:
            return False

        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.isfile(file):
            os.remove(file)

        try:
            session.retrbinary('RETR %s' % filename, open(file, "wb").write)
            session.close
            return file
        except:
            session.close
            return False

