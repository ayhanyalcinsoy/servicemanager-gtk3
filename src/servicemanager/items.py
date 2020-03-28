#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

class listServices(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(10)
        hbox = Gtk.Box(spacing = 1)
        hbox.set_homogeneous(False)

        vbox_flag = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=1)
        vbox_flag.set_homogeneous(False)
        hbox.pack_start(vbox_flag, True, True, 0)

        image = Gtk.Image()
        image.set_from_icon_name("flag-yellow", 64)
        vbox_flag.pack_start(image, True, True, 0)

        vbox_service = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_service.set_homogeneous(False)
        hbox.pack_start(vbox_service, True, True, 0)

        serviceName = Gtk.Label("Docker")
        vbox_service.pack_start(serviceName, True, True, 0)

        serviceDesc = Gtk.Label("Docker Yönetim Hizmeti")
        vbox_service.pack_start(serviceDesc, True, True, 0)

        vbox_space = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_space.set_homogeneous(False)
        hbox.pack_start(vbox_space, True, True, 0)

        space = Gtk.Fixed()
        space.put(Gtk.Label(), 0, 1)
        vbox_space.pack_start(space, True, True, 0)

        vbox_start = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_start.set_homogeneous(False)
        hbox.pack_start(vbox_start, True, True, 0)

        btn_Start = Gtk.Button.new_from_icon_name("media-playback-start", 22)
        vbox_start.pack_start(btn_Start,True, True, 0)

        vbox_stop = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_stop.set_homogeneous(False)
        hbox.pack_start(vbox_stop, True, True, 0)

        btn_Stop = Gtk.Button.new_from_icon_name("media-playback-stop", 32)
        # btn_Start.connect("clicked", self.startServices)
        vbox_stop.pack_start(btn_Stop, True, True, 0)

        vbox_reload = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_reload.set_homogeneous(False)
        hbox.pack_start(vbox_reload, True, True, 0)

        btn_Reload = Gtk.Button.new_from_icon_name("media-playlist-repeat", 22)
        # btn_Start.connect("clicked", self.startServices)
        vbox_reload.pack_start(btn_Reload, True, True, 0)

        vbox_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_info.set_homogeneous(False)
        hbox.pack_start(vbox_info, True, True, 0)

        btn_Info = Gtk.Button.new_from_icon_name("gtk-info", 22)
        # btn_Start.connect("clicked", self.startServices)
        vbox_info.pack_start(btn_Info, True, True, 0)

        vbox_checkService = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox_checkService.set_homogeneous(False)
        hbox.pack_start(vbox_checkService, True, True, 0)

        btn_checkService = Gtk.CheckButton("Run Start On")
        btn_checkService.set_active(True)
        #btn_checkService.connect("clicked", self.on_clicked)
        vbox_checkService.pack_start(btn_checkService, True, True, 0)

        self.add(hbox)



win = listServices()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
