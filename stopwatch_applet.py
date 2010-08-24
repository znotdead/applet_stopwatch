#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject
import time
import sys


class Stopwatch():
    def __init__(self, applet, iid):
        # [some instance variable definitions]
        self.state = 0 # 0 means stopwatch is stopped, 1 started
        self.start_time = 0
        self.elapsed_time = 0
        self.timeout_interval = 10000

        # [widget definitions]
        self.vbox = gtk.VBox()
        self.label = gtk.Label('0h 0m 0s')
        self.button_start_stop = gtk.Button(label='Start/Stop')
        self.button_start_stop.connect('clicked',  self.start_stop)
        self.button_pause = gtk.Button(label='Pause')
        self.button_pause.connect('clicked', self.pause)
        self.vbox.add(self.label)
        self.vbox.add(self.button_start_stop)
        self.vbox.add(self.button_pause)
        applet.add(self.vbox)

        gobject.timeout_add(self.timeout_interval, self.timeout_callback, self)


    def timeout_callback(self, event):
        if self.state:
            self.label.set_label(self._sec_to_human(self.elapsed()))
        return 1

    def elapsed(self):
        return time.time() - self.start_time + self.elapsed_time

    # callback to start and stop watch
    def start_stop(self, widget):
        if self.state:
            self.stop()
        else:
            self.start()

    # callback for pause button
    def pause(self, widget):
        self.state = 0
        self.elapsed_time = time.time() - self.start_time

    # set state to 1 and begins updating UI
    def start(self):
        self.state = 1
        self.start_time = time.time()
        self.timeout_callback(self)

    #  set state to 0 to stop timer
    def stop(self):
        self.state = 0
        self.elapsed_time = 0




    #@staticmethod
    def _sec_to_human(self, sec):
        hours, rest = divmod(sec, 3600)
        minutes, sec = divmod(rest, 60)
        return 'H: %s M: %s S: %s' % (str(int(hours)), str(int(minutes)), str(int(sec)))



# bonobo factory
def stopwatch_applet_factory(applet, iid):
    stopwatch = Stopwatch(applet,iid)
    return gtk.TRUE

if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title("Python Applet Stopwatch")
        main_window.connect("destroy", gtk.main_quit)
        app = gnomeapplet.Applet()
        stopwatch_applet_factory(app, None)
        app.reparent(main_window)
        main_window.show_all()
        gtk.main()
        sys.exit()


print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_PythonAppletStopwatch_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", stopwatch_applet_factory)
print "Factory ended"
