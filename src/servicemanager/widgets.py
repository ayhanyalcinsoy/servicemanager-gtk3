#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PDS Stuff
#from pds.gui import *
import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository import GObject
# Python Stuff
import time
import textwrap
import locale

# Pisi Stuff
import sys
import pisi

#from servicemanager.item import listServices

class ServiceItem(Gtk.ListBoxRow):

    def __init__(self, package, parent):
        Gtk.ListBoxRow.__init__(self, parent)

        self.package = package

class ServiceItemWidget(Gtk.ListBox):

    def __init__(self, package, parent, item):
        Gtk.ListBoxRow.__init__(self, None)

        self.ui = listServices()
        self.ui.SetupUi(self)

        self.serviceName.setText(package)
        self.service_on_of(self, toggle=False)

        self.toggled = False
        self.root = parent
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.info = ServiceItemInfo(self)


        self.type = None
        self.desc = None
        self.service_on_of.set_active(self.setService)
        self.service_on_of.set_state(self.setService)
        self.service_Reload.connect("clicked", self.setService)
        self.checkStart.connec("clicked", self.setService)
        self.service_Info.connect("clicked",self.info.showDescription)
class Handler:
    def updateService(self, data, firstRun):
        self.type, self.desc, serviceState = data
        self.setState(serviceState, firstRun)
        self.serviceDesc.setText(self.desc)

    def setState(self, state, firstRun=False):
        if not firstRun:
            # There is a raise condition, FIXME in System.Service
            time.sleep(1)
            state = self.iface.info(self.package)[2]
        if state in ('on', 'started', 'conditional_started'):
            self.running = True
            icon = 'flag-green'
        else:
            self.running = False
            icon = 'flag-black'

        self.service_on_of.setEnabled(self.running)
        self.service_Reload.setEnabled(self.running)

        self.labelStatus.set_icon(icon)
        self.showStatus()
        self.runningAtStart = False
        if state in ('on', 'stopped'):
            self.runningAtStart = True
        elif state in ('off', 'started', 'conditional_started'):
            self.runningAtStart = False
        self.checkStart.setChecked(self.runningAtStart)
        self._last_state = self.checkStart.isChecked()
        # print self.package, state

    def setService(self):
        try:
            self.showBusy()
            self._last_state = not self.checkStart.isChecked()
            if self.sender() == self.service_on_of.set_active():
                self.iface.start(self.package)
            elif self.sender() == self.service_on_of.set_state():
                self.iface.stop(self.package)
            elif self.sender() == self.service_Reload:
                self.iface.restart(self.package)
            elif self.sender() == self.checkStart:
                self.iface.setEnable(self.package, self.checkStart.isChecked())
        except Exception as msg:
            self.showStatus()
            self.root.showFail(msg)

    def switchToOld(self):
        self.checkStart.setChecked(self._last_state)

    def showStatus(self):
        self.busy.hide()
        self.labelStatus.show()

    def showBusy(self):
        self.busy.busy()
        self.labelStatus.hide()

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.service_on_of.set_active(setVisible(toggle))
        self.service_on_of.set_state(setVisible(toggle))
        self.service_Reload.setVisible(toggle)
        self.service_Info.setVisible(toggle)
        self.checkStart.setVisible(toggle)

def getDescription(service):
    try:
        # TODO add a package map for known services
        service = service.replace('_','-')
        lang = str(locale.getdefaultlocale()[0].split("_")[0])
        desc = pisi.api.info_name(service)[0].package.description
        if desc.has_key(lang):
            return str(desc[lang])
        return str(desc['en'])
    except Exception as msg:
        # print "ERROR:", msg
        return unicode(i18n('Service information is not available'))
    '''
class ServiceItemInfo(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent)

        self.ui.buttonHide.clicked.connect(self.hideDescription)
        self.ui.buttonHide.set_icon_name("dialog-close")

        self._animation = 2
        self._duration = 500

        self.enableOverlay()
        self.hide()

    def showDescription(self):
        self.resize(self.parentWidget().size())
        desc = getDescription(self.parentWidget().package)
        self.ui.description.setText(desc)
        self.ui.description.setToolTip('\n'.join(textwrap.wrap(desc)))
        self.animate(start = MIDLEFT, stop = MIDCENTER)
        #Gtk.Application.
        #QtWidgets.qApp.processEvents()


    def hideDescription(self):
        if self.isVisible():
            self.animate(start = MIDCENTER,
                         stop  = MIDRIGHT,
                         direction = OUT)

'''
builder = Gtk.Builder()
builder.add_from_file("../ui/item.ui")
builder.connect_signals(Handler())
window = builder.get_object("listServices")
#window.connect("destroy", Gtk.main_quit)
#window.show_all()
#Gtk.main()