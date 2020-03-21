#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
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
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from servicemanager.mainwindow import MainWindow




if __name__ == "__main__":
    app = MainWindow()
    app.run(sys.argv)
