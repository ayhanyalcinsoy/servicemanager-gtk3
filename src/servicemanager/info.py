#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler:
    def on_quit(self, btn_ok):
        self.destroy()

class ServiceInfo(Gtk.Widget) :
    def __init__(self):
        Gtk.Widget.__init__(self)
        info = Gtk.Builder()
        info.add_from_file("./ui/info.glade")
        window = info.get_object("WindowInf")
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        Handlers = {
            "on_quit": Gtk.main_quit
             }
        info.connect_signals(Handlers)
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        Gtk.main()