#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from about import AboutDialog
from info import ServiceInfo

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

    def showStatus(self):
        self.busy.hide()
        self.labelStatus.show()

    def getDescription(service):
        try:
            # TODO add a package map for known services
            service = service.replace('_', '-')
            lang = str(locale.getdefaultlocale()[0].split("_")[0])
            desc = pisi.api.info_name(service)[0].package.description
            if desc.has_key(lang):
                return str(desc[lang])
            return str(desc['en'])
        except Exception as msg:
            # print "ERROR:", msg
            return unicode(i18n('Service information is not available'))

    def on_btn_start(self, btn_start):
        print "start"

    def on_btn_stop(self, btn_stop):
        print "stop"

    def on_btn_reload(self, btn_reload):
        print "reload"

    def on_btn_info(self, btn_info):
        ServiceInfo()

    def on_about(self, about):
        aboutdialog = AboutDialog()
        aboutdialog.run()

    def on_exit(self, exit):
        Gtk.main_quit()



builder = Gtk.Builder()
builder.add_from_file("./ui/main.glade")
builder.connect_signals(Handler())
window = builder.get_object("MainWindow")

window.show_all()
Gtk.main()
