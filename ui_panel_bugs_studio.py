#! /usr/bin/env python3
# coding: utf-8

bl_info = {
    'name': 'Bugs studio',
    'description': 'Connexion website',
    'author': 'Yohan Solon',
    'license': 'GPL',
    'deps': '',
    'version': (1, 2, 8),
    'blender': (2, 7, 9),
    'location': 'BugsStudio',
    'warning': '',
    'wiki_url': 'https://github.com/s-leger/archipack/wiki',
    'tracker_url': 'https://github.com/milimi974/OC_Projet_13/issues',
    'link': 'https://github.com/milimi974/OC_Projet_13',
    'category': 'YOHAN',
    }

import bpy
from bpy.types import Panel, AddonPreferences, UIList
from bpy.props import (
    EnumProperty, PointerProperty,
    StringProperty, BoolProperty,
    IntProperty, FloatProperty, FloatVectorProperty
    )
import requests
import urllib
from ftplib import FTP
import json
from datetime import datetime

# ----------------------------------------------------
# Addon preferences
# ----------------------------------------------------


class Bugs_Pref(AddonPreferences):
    bl_idname = __name__
    # calendar json file url
    json_url = StringProperty(
        name="JSON Uri",
        description="Add json file url",
        default="http://www.mywebsite.fr/json.php",
    )
    # ftp server host
    ftp_hostname = StringProperty(
        name="FTP Hostname",
        description="Add FTP hostname",
        default="www.mywebsiteftp.fr",
    )
    # ftp server login
    ftp_login = StringProperty(
        name="FTP Login",
        description="Add FTP user login",
        default="My Login",
    )
    # ftp server password
    ftp_password = StringProperty(
        name="FTP Password",
        description="Add FTP user password",
        default="**********",
    )
    # ftp server port
    ftp_port = StringProperty(
        name="FTP Port",
        description="Add FTP port server",
        default="21",
    )

    def draw(self, context):
        layout = self.layout
        # Section JSON management view
        box = layout.box()
        row = box.row()
        col = row.column()
        col.label(text="Tab Json:")
        col.prop(self, "json_url")
        # Section FTP management view
        box = layout.box()
        box.label("FTP")
        row = box.row()
        col = row.column()
        col.prop(self, "ftp_hostname")
        col.prop(self, "ftp_port")
        col.prop(self, "ftp_login")
        col.prop(self, "ftp_password")


# ----------------------------------------------------
# Request api url/ftp
# ----------------------------------------------------


class BugsApi:
    """ this class manage api connexion """

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
            response = session.storbinary('STOR {}{}'.format(ftp_subpath+"/", filename), file)  # send the file
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
    def DownloadMesh(self, filename, subpath=""):
        urllib.urlretrieve(self.ftp_host + subpath, filename)


class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

# ----------------------------------------------------
# Calendar Panel
# ----------------------------------------------------


# Class for the panel inherit Panel
class BugsPanelCalendar(View3DPanel, Panel):
    """ this are a custom panel viewport """
    bl_label = 'Calendar'
    bl_context = 'objectmode'
    bl_category = 'Bugs Studio'


    # Add UI Elements
    def draw(self, context):
        layout = self.layout
        # plugin prefs
        prefs = context.user_preferences.addons[__name__].preferences

        # Section FTP management view
        box = layout.box()
        box.label("FTP")
        row = box.row()
        col = row.column()
        api = BugsApi(prefs.json_url, prefs.ftp_hostname, prefs.ftp_login, prefs.ftp_password, prefs.ftp_port)
        dates = api.GetCalendar()
        # Section Calendar management view
        layout.label(text='Prochaine date')
        box = layout.box()
        now = datetime.now()
        first = True
        for date in dates:
            ob_date = datetime.strptime(date, "%d %m %Y")
            if ob_date > now:
                if first:
                    box.label(ob_date.strftime('Samedi %d %B %Y'), icon='COLOR_GREEN')
                    first = False
                else:
                    box.label(ob_date.strftime('Samedi %d %B %Y'), icon='SORTTIME')

# ----------------------------------------------------
# Mesh Panel
# ----------------------------------------------------


# Class for the panel inherit Panel
class BugsPanelMesh(View3DPanel, Panel):
    """ this are a custom panel viewport """
    bl_label = 'Online Mesh'
    bl_context = 'objectmode'
    bl_category = 'Bugs Studio'

    # Add UI Elements
    def draw(self, context):
        layout = self.layout
        # plugin prefs
        prefs = context.user_preferences.addons[__name__].preferences

        # Section FTP management view
        box = layout.box()
        box.label("FTP")
        row = box.row()
        col = row.column()
        api = BugsApi(prefs.json_url, prefs.ftp_hostname, prefs.ftp_login, prefs.ftp_password, prefs.ftp_port)

        layout.label(text='Dates bugs')
        layout.operator("mesh.primitive_cube_add", text="Cube")
        layout.label(text='Mesh disponible')


# Register
def register():
    bpy.utils.register_class(BugsPanelCalendar)
    bpy.utils.register_class(BugsPanelMesh)
    bpy.utils.register_class(Bugs_Pref)


# Unregister
def unregister():
    bpy.utils.unregister_class(BugsPanelCalendar)
    bpy.utils.unregister_class(BugsPanelMesh)
    bpy.utils.unregister_class(Bugs_Pref)


if __name__ == "__main__":
    register()

