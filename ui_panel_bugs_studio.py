#! /usr/bin/env python3
# coding: utf-8

bl_info = {
    'name': 'Bugs studio',
    'description': 'Connexion website',
    'author': 'Yohan Solon',
    'license': 'GPL',
    'deps': '',
    'version': (1, 0, 0),
    'blender': (2, 7, 9),
    'location': 'BugsStudio',
    'warning': '',
    'wiki_url': 'https://github.com/s-leger/archipack/wiki',
    'tracker_url': 'https://github.com/milimi974/OC_Projet_13/issues',
    'link': 'https://github.com/milimi974/OC_Projet_13',
    'category': 'YOHAN',
    }

import bpy
from bpy.types import Panel, AddonPreferences, UIList, Operator
from bpy.props import (
    EnumProperty, PointerProperty,
    StringProperty, BoolProperty,
    IntProperty, FloatProperty, FloatVectorProperty
    )
import requests
import os
from ftplib import FTP
import json
from datetime import datetime


# ----------------------------------------------------
# custom list manager
# ----------------------------------------------------
class BugsMeshGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()


bpy.utils.register_class(BugsMeshGroup)
bpy.types.Scene.bugsMeshLists = bpy.props.CollectionProperty(type=BugsMeshGroup)


class BugsCalendarGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()


bpy.utils.register_class(BugsCalendarGroup)
bpy.types.Scene.bugsCalendarLists = bpy.props.CollectionProperty(type=BugsCalendarGroup)

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


class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

# ----------------------------------------------------
# Calendar Panel
# ----------------------------------------------------


# plugin prefs

now = datetime.now()
for date in dates:
    ob_date = datetime.strptime(date, "%d %m %Y")
    if ob_date > now:
        newItem = bpy.context.scene.bugsCalendarLists.add()
        newItem.day = date


# this operator load calendar valide date
class LoadCalendarOperator(Operator):
    bl_idname = "wm.load_calendar"
    bl_label = ""

    def execute(self, context):
        if len(context.scene.bugsCalendarLists) == 0:
            prefs = bpy.context.user_preferences.addons[__name__].preferences
            api = BugsApi(prefs.json_url, prefs.ftp_hostname, prefs.ftp_login, prefs.ftp_password, prefs.ftp_port)
            dates = api.GetCalendar()
            now = datetime.now()
            for date in dates:
                ob_date = datetime.strptime(date, "%d %m %Y")
                if ob_date > now:
                    newItem = context.scene.bugsCalendarLists.add()
                    newItem.day = ob_date.strftime('Samedi %d %B %Y')

        return {'FINISHED'}

bpy.ops.wm.load_calendar()


# Class for the panel inherit Panel
class BugsPanelCalendar(View3DPanel, Panel):
    """ this are a custom panel viewport """
    bl_label = 'Calendrier'
    bl_context = 'objectmode'
    bl_category = 'Bugs Studio'

    # Add UI Elements
    def draw(self, context):
        layout = self.layout
        # Section Calendar management view
        layout.label(text='Prochaine date')
        box = layout.box()
        first = True
        for date in context.scene.bugsCalendarLists:
            if first:
                box.label(date.day, icon='COLOR_GREEN')
                first = False
            else:
                box.label(date.day, icon='SORTTIME')

# ----------------------------------------------------
# Mesh Panel
# ----------------------------------------------------


# manage upload mesh
class RefreshOnlineMeshOperator(Operator):
    bl_idname = "bugs.refresh_online_mesh"
    bl_label = ""

    mesh_name = bpy.props.StringProperty()  # defining the property

    def execute(self, context):
        # plugin prefs
        prefs = context.user_preferences.addons[__name__].preferences

        # Section FTP management view
        api = BugsApi(prefs.json_url, prefs.ftp_hostname, prefs.ftp_login, prefs.ftp_password, prefs.ftp_port)

        context['bugs_online_mesh'] = api.GetFtpMeshList("mesh")

        return {'FINISHED'}

# download mesh from ftp
class GetOnlineMeshOperator(Operator):
    bl_idname = "bugs.get_online_mesh"
    bl_label = ""

    mesh_name = bpy.props.StringProperty()  # defining the property

    def execute(self, context):
        prefs = context.user_preferences.addons[__name__].preferences
        api = BugsApi(prefs.json_url, prefs.ftp_hostname, prefs.ftp_login, prefs.ftp_password, prefs.ftp_port)
        mesh = api.DownloadMesh(self.mesh_name, "mesh")
        return {'FINISHED'}


# Class for the panel inherit Panel
class BugsPanelMesh(View3DPanel, Panel):
    """ this are a custom panel viewport """
    bl_label = 'Mesh en ligne'
    bl_context = 'objectmode'
    bl_category = 'Bugs Studio'

    # Add UI Elements
    def draw(self, context):
        layout = self.layout
        files = []
        if context.bugs_online_mesh:
            files = context.bugs_online_mesh

        # Section FTP management view
        box = layout.box()
        col = box.column()
        # add mesh operator
        for mesh in files:
            op = col.operator("bugs.get_online_mesh", text=mesh, icon="OUTLINER_OB_GROUP_INSTANCE")
            op.mesh_name = mesh


# Register
def register():
    bpy.utils.register_class(LoadCalendarOperator)
    bpy.utils.register_class(RefreshOnlineMeshOperator)
    bpy.utils.register_class(GetOnlineMeshOperator)
    bpy.utils.register_class(BugsPanelCalendar)
    bpy.utils.register_class(BugsPanelMesh)
    bpy.utils.register_class(Bugs_Pref)


# Unregister
def unregister():
    bpy.utils.unregister_class(LoadCalendarOperator)
    bpy.utils.unregister_class(RefreshOnlineMeshOperator)
    bpy.utils.unregister_class(GetOnlineMeshOperator)
    bpy.utils.unregister_class(BugsPanelCalendar)
    bpy.utils.unregister_class(BugsPanelMesh)
    bpy.utils.unregister_class(Bugs_Pref)


if __name__ == "__main__":
    register()

