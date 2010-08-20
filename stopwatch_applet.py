#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject

import sys

def background_show(applet):
    print "background: ", applet.get_background()

def sample_factory(applet, iid):
    print "Creating new applet instance"

    label = gtk.Label("Success!")
    applet.add(label)
    applet.show_all()
    gobject.timeout_add(1000, background_show, applet)
    return True


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title("Python Applet")
        main_window.connect("destroy", gtk.mainquit)
        app = gnomeapplet.Applet()
        sample_factory(app, None)
        app.reparent(main_window)
        main_window.show_all()
        gtk.main()
        sys.exit()

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_PythonAppletStopwatch_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
