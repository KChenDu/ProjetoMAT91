from window import MatWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = MatWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
