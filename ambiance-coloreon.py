import re, os
from gi.repository import GLib, Gio, GObject
import shutil
import gconf

USER = os.getenv('USER')
GSETTINGS = Gio.Settings.new("org.gnome.desktop.interface")
GCONF = gconf.client_get_default()

def change_theme(color_hex):
	write_changes(color_hex)
	GCONF.set_string("/apps/metacity/general/theme", "Ambiance")
	GSETTINGS.set_string("gtk-theme", "Ambiance")
	GSETTINGS.set_string("gtk-theme", "Ambiance-chameleon")

def write_changes(color_hex):
	try:
		shutil.copytree("/usr/share/themes/Ambiance", "/home/%s/.themes/Ambiance-chameleon" % USER)
	except:
		pass
	print "Changing the highlight to #"+color_hex
	with open("/home/%s/.themes/Ambiance-chameleon/gtk-3.0/gtk.css" % USER, "r") as sources:
		lines = sources.readlines()
	with open("/home/%s/.themes/Ambiance-chameleon/gtk-3.0/gtk.css" % USER, "w") as sources:
		for line in lines:
			if line.startswith('@define-color selected_bg_color '):
				line = re.sub(r'#.+',r'#'+color_hex+';', line)
			sources.write(line)

	with open("/home/%s/.themes/Ambiance-chameleon/gtk-2.0/gtkrc" % USER, "r") as sources:
		lines = sources.readlines()
	with open("/home/%s/.themes/Ambiance-chameleon/gtk-2.0/gtkrc" % USER, "w") as sources:
		for line in lines:
			if line.startswith('gtk-color-scheme = '):
				line = re.sub(r'selected_bg_color:#[\w]+',r'selected_bg_color:#'+color_hex, line)
			sources.write(line)

change_theme("FF5533")
