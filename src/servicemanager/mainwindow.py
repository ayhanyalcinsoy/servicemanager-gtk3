#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib

from backend import ServiceIface
from about import AboutDialog
from widgets import ServiceItem, ServiceItemWidget


class MainWindow(Gtk.Application):
    def __init__(self, *args, **kwargs):
        Gtk.Application.__init__(self)

        # Call Comar
        self.iface = ServiceIface(self.exceptionHandler)
        self.widgets = {}

        # Fill service list
        self.services = self.iface.services()
        self.services.sort()

        for service in self.services:
            item = ServiceItem(service, self.listServices)
            item.setFlags(Gtk.NoItemFlags | Gtk.ItemIsEnabled)
            item.setSizeHint(Gtk.size(38, 48))
            self.widgets[service] = ServiceItemWidget(service, self, item)
            self.listServices.setItemWidget(item, self.widgets[service])
        self.infoCount = 0
        self.piece = 100 / len(self.services)

        # Update service status and follow Comar for state changes
        self.getServices()

        # search line, we may use model view for correct filtering
        self.lineSearch.textChanged[str].connect(self.doSearch)
        self.filterBox.currentIndexChanged[int].connect(self.filterServices)

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
        messageBox = Gtk.MessageDialog(self, GTK_MESSAGE_ERROR, GTK_BUTTON_CLOSE, errorTitle)

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

    def on_about(self, about):
        about_dialog = AboutDialog()
        about_dialog.run()

    def on_quit(self, exit):
        Gtk.main_quit()

class Handler:
    def on_about(self, about):
        about_dialog = AboutDialog()
        about_dialog.run()

    def on_quit(self, exit):
        Gtk.main_quit()



builder = Gtk.Builder()
builder.add_from_file("../ui/main.ui")
builder.connect_signals(Handler())
window = builder.get_object("MainWindow")
window.set_icon_from_file("../data/flag-yellow.png")
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()