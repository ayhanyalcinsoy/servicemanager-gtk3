#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class serviceItem(Gtk.Widget):
    def __init__(self):
        Gtk.Widget.__init__(self)
        item = Gtk.Builder()
        item.add_from_file("../ui/item.glade")
        window = item.get_object("listServices")
        window.connect("destroy", Gtk.main_quit)
        window.show_all()