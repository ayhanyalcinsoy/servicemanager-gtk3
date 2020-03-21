#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class AboutDialog(Gtk.AboutDialog) :
    def __init__(self):
        Gtk.AboutDialog.__init__(self)
        self.set_title("Service Manager")
        self.set_program_name("Service Manager")
        self.set_version("3.1.1")
        self.set_comments("Service Manager is an application for managing system services. It uses COMAR as configuration backend.")
        self.set_website("https://www.pisilinux.org")
        self.set_logo_icon_name("flag-yellow")
        self.set_authors([":","Gökmen Göksel","Bahadır Kandemir","Ayhan Yalçınsoy"])
        self.connect("response", self.on_response)

    def on_response(self, dialog, repsonse):
        self.destroy()


about_dialog = AboutDialog()
#about_dialog.run()