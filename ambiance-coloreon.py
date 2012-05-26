#!/usr/bin/env python

import re, os, sys
from gi.repository import GLib, Gio, GObject
import shutil
import gconf

USER = os.getenv('USER')
GSETTINGS = Gio.Settings.new("org.gnome.desktop.interface")
GCONF = gconf.client_get_default()



def parse_color_hex(argument):

	"""Parses a string, which may just as well be a system argument, for a hash-less hexadecimal encoded color string."""
	
	color_hex = argument
	
	#clean
	#count
	#lowercase
	#characters
	
	return color_hex
	

def colorize_gtk_theme(color_hex):

	"""This function colorizes Ambience GTK theme given a hexadecimal color value as a string.
	
	It first duplicates the original theme to the user's theme override directory.
	And then replaces all ocurrences of the highlight color to that supplied by its argument.	
	"""

	try:
		shutil.copytree("/usr/share/themes/Ambiance", "/home/%s/.themes/Ambiance-coloreon" % USER)
	except:
		pass
	
	with open("/home/%s/.themes/Ambiance-coloreon/gtk-3.0/gtk.css" % USER, "r") as sources:
		lines = sources.readlines()
	with open("/home/%s/.themes/Ambiance-coloreon/gtk-3.0/gtk.css" % USER, "w") as sources:
		for line in lines:
			if line.startswith('@define-color selected_bg_color '):
				line = re.sub(r'#.+',r'#'+color_hex+';', line)
			sources.write(line)

	with open("/home/%s/.themes/Ambiance-coloreon/gtk-2.0/gtkrc" % USER, "r") as sources:
		lines = sources.readlines()
	with open("/home/%s/.themes/Ambiance-coloreon/gtk-2.0/gtkrc" % USER, "w") as sources:
		for line in lines:
			if line.startswith('gtk-color-scheme = '):
				line = re.sub(r'selected_bg_color:#[\w]+',r'selected_bg_color:#'+color_hex, line)
			sources.write(line)


def colorize_metacity_theme(color_hex):

	"""This function colorizes the Ambience Metacity theme.
	
	Except it that it does't, yet.
	"""
	
	pass
	
	
def reset_theme():

	"""Sets the user's themes to the default Ambience ones."""

	GSETTINGS.set_string("gtk-theme", "Ambiance")
	GCONF.set_string("/apps/metacity/general/theme", "Ambiance")


def change_theme():

	"""Sets the user's themes to the colorized ones, or the defaults, failing that."""
	
	reset_theme()
	
	GSETTINGS.set_string("gtk-theme", "Ambiance-coloreon")
	GCONF.set_string("/apps/metacity/general/theme", "Ambiance")
	
	
	
colorize_gtk_theme(parse_color_hex(sys.argv[1]))
change_theme()
