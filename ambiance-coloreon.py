#!/usr/bin/env python

import re, os, sys
from gi.repository import GLib, Gio, GObject
import shutil
import gconf
import colorsys

USER = os.getenv('USER')
GSETTINGS = Gio.Settings.new("org.gnome.desktop.interface")
GCONF = gconf.client_get_default()



def parse_color_hex(argument):

	"""Parses a string, which may just as well be a system argument, for a hash-less hexadecimal encoded color string."""
	
	if len(argument) != 6:
		raise Exception("Color value is not the right length!")
	else:
		if False in [i in "0123456789abcdef" for i in argument.lower()]:
			raise Exception("Color value contains characters outside of hexadecimal!")
		else:
			return argument
	

def colorize_gtk_theme(color_hex):

	"""This function colorizes Ambiance GTK theme given a hexadecimal color value as a string.
	
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

	"""This function colorizes the Ambiance Metacity theme.
	
	It first converts the chosen color to HSV, and calculates the offset values for Imagemagick.
	Then, it duplicates all the colored images from Ambiance to Ambiance-coloreon anew,
	converts them to RGBA and applies the ImageMagick modulation function on them.
	"""
	
	aubergine_hsv = (0.055, 0.98, 0.88) #e04d04
	
	color_rgb = ( int(color_hex[0:2], 16),
                  int(color_hex[2:4], 16),
                  int(color_hex[4:6], 16) )       
	color_hsv = colorsys.rgb_to_hsv( *[ color/255.0 for color in color_rgb ] )
	
	# Generating the values needed for ImageMagick modulate:
	# Brightness/Value should remain constant.
	# In ImageMagick-land, the hue-space is a total of 200.
	# But in regular HSV-land, it is 1.
	# Hence the seemingly ugly expression.

	im_bsh = ( 100, 													#brightness or value
           	   100 + int( (color_hsv[1] - aubergine_hsv[1]) * 100 ), 	#saturation
           	   300 + int( (color_hsv[0] - aubergine_hsv[0]) * 200 ) ) 	#hue
	
	image_list = [
		"metacity-1/close.png",
		"metacity-1/close_focused_normal.png",
		"metacity-1/close_focused_prelight.png",
		"metacity-1/close_focused_pressed.png",
		"unity/close.png",
		"unity/close_focused_normal.png",
		"unity/close_focused_prelight.png",
		"unity/close_focused_pressed.png",
	]
	
	for image in image_list:
		source = "/usr/share/themes/Ambiance/"+image
		local = "/home/"+USER+"/.themes/Ambiance-coloreon/"+image
		os.system( "cp %s %s" % (source, local) )
		os.system( "convert %s -colorspace RGB %s" % (local, local) )
		os.system( "convert %s -set option:modulate:colorspace hsb -modulate %s,%s,%s %s" % (local, im_bsh[0], im_bsh[1], im_bsh[2], local) )
	
	
def reset_theme():

	"""Sets the user's themes to the default Ambiance ones."""

	GSETTINGS.set_string("gtk-theme", "Ambiance")
	GCONF.set_string("/apps/metacity/general/theme", "Ambiance")


def change_theme():

	"""Sets the user's themes to the colorized ones, or the defaults, failing that."""
	
	reset_theme()
	
	GSETTINGS.set_string("gtk-theme", "Ambiance-coloreon")
	GCONF.set_string("/apps/metacity/general/theme", "Ambiance-coloreon")
	
	
	
colorize_gtk_theme(parse_color_hex(sys.argv[1]))
colorize_metacity_theme(parse_color_hex(sys.argv[1]))
change_theme()
