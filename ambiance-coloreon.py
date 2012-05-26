import re, os
from gi.repository import GLib, Gio, GObject
import shutil
import gconf
import time

USER = os.getenv('USER')
BG = Gio.Settings.new("org.gnome.desktop.background")
GSETTINGS = Gio.Settings.new("org.gnome.desktop.interface")
GCONF = gconf.client_get_default()

class Daemon:
    def __init__ (self):
        BG.connect("changed::picture-uri", self.change_theme)

    def change_theme (self, *_):
        print "Waiting a few seconds before applying the changes..."
        time.sleep(3)
        self.write_changes(self.get_color ())
        GCONF.set_string("/apps/metacity/general/theme", "Ambiance")
        GSETTINGS.set_string("gtk-theme", "Ambiance")
        GSETTINGS.set_string("gtk-theme", "Ambiance-chameleon")

    def get_color (self):
        xprop_value = GLib.spawn_command_line_sync("/usr/bin/xprop -root _GNOME_BACKGROUND_REPRESENTATIVE_COLORS")
        rgb_set = re.match(r".*\((\d+)\,(\d+),(\d+).*", xprop_value[1]).groups ()
        color_hex = '%02x%02x%02x' % (int(rgb_set[0]), int(rgb_set[1]), int(rgb_set[2]))
        return str(color_hex)

    def write_changes (self, color_hex):
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

if __name__ == "__main__":
    daemon = Daemon()
    GObject.MainLoop().run()
