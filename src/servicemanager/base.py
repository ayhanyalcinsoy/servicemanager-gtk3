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

# System
import sys
import comar
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
# Qt Stuff
#from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QMessageBox
#from PyQt5.QtCore import *

# Application Stuff
from servicemanager.backend import ServiceIface
from servicemanager.ui_main import Ui_mainManager
from servicemanager.widgets import ServiceItemWidget, ServiceItem

class MainManager(Gtk.Widget):
    def __init__(self, parent, standAlone=True):
        Gtk.widgets.__init__(self,parent)

        # Create the ui
        self.ui = Ui_mainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        # Call Comar
        self.iface = ServiceIface(self.exceptionHandler)
        self.widgets = {}

        # Fill service list
        self.services = self.iface.services()
        self.services.sort()
        for service in self.services:
            item = ServiceItem(service, self.ui.listServices)
            item.setFlags(Gtk.NoItemFlags | Gtk.ItemIsEnabled)
            item.setSizeHint(Gtk.size(38,48))
            self.widgets[service] = ServiceItemWidget(service, self, item)
            self.ui.listServices.setItemWidget(item, self.widgets[service])
        self.infoCount = 0
        self.piece = 100/len(self.services)

        # Update service status and follow Comar for state changes
        self.getServices()

        # search line, we may use model view for correct filtering
        self.ui.lineSearch.textChanged[str].connect(self.doSearch)
        self.ui.filterBox.currentIndexChanged[int].connect(self.filterServices)

    def hiddenListWorkaround(self):
        """
            Workaround for hidden list items
        """
        size = self.size()
        size += Gtk.size(1,1)
        Gtk.timer.singleShot(1, lambda: self.resize(size))
        size -= Gtk.size(1,1)
        Gtk.timer.singleShot(5, lambda: self.resize(size))

    def doSearch(self, text):
        for service in self.services:
            if service.find(text) >= 0 or str(self.widgets[service].desc).lower().find(str(text).lower()) >= 0:
                self.widgets[service].item.setHidden(False)
            else:
                self.widgets[service].item.setHidden(True)
        if text == '':
            self.filterServices(self.ui.filterBox.currentIndex())

        self.hiddenListWorkaround()

    def isLocal(self, service):
        return self.widgets[service].type == 'local'

    def showFail(self, exception):

        exception = str(exception)
        if exception.startswith('tr.org.pardus.comar.Comar.PolicyKit'):
            errorTitle = i18n("Authentication Error")
            errorMessage = i18n("You are not authorized for this operation.")
        else:
            errorTitle = i18n("Error")
            errorMessage = i18n("An exception occurred.")
        messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)

        if not exception.startswith('tr.org.pardus.comar.Comar.PolicyKit'):
            messageBox.setDetailedText(unicode(exception))

        messageBox.exec_()

    def filterServices(self, filterBy):
        Servers, SystemServices, StartupServices, RunningServices, AllServices = range(5)
        for service in self.services:
            if filterBy == Servers:
                if not self.isLocal(service):
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == SystemServices:
                if self.isLocal(service):
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == StartupServices:
                if self.widgets[service].runningAtStart:
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == RunningServices:
                if self.widgets[service].running:
                    self.widgets[service].item.setHidden(False)
                else:
                    self.widgets[service].item.setHidden(True)
            elif filterBy == AllServices:
                self.widgets[service].item.setHidden(False)

        self.hiddenListWorkaround()

    def handleServices(self, package, exception, results):
        # Handle request and fill the listServices in the ui
        if not exception:
            self.widgets[package].updateService(results, True)
            self.infoCount += 1
            self.ui.progress.setValue(self.ui.progress.value() + self.piece)
            if self.infoCount == len(self.services):
                self.ui.progress.hide()
                self.ui.listServices.setEnabled(True)
                self.filterServices(self.ui.filterBox.currentIndex())
                self.doSearch(self.ui.lineSearch.text())

    def getServices(self):
        self.iface.services(self.handleServices)
        self.iface.listen(self.handler)

    def handler(self, package, signal, args):
        # print "COMAR :", args, signal, package
        self.widgets[package].setState(args[1])
        self.filterServices(self.ui.filterBox.currentIndex())
        self.doSearch(self.ui.lineSearch.text())

    def exceptionHandler(self, package, exception, args):
        if exception:
            if package in self.widgets:
                self.widgets[package].showStatus()
                self.widgets[package].switchToOld()
            self.showFail(exception)

    def event(widget, event):
        if event.button == 3:
            menu.popup(None, None, None, None, event.button, event.time)
            menu.show_all()





