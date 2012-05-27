Ambience Coloreon
=================

(Or Coloreonic Ambience, if you prefer.)

Ambience-Coloreon is a dumbed-down version of the _lovely_ script by **David Callé**, [Chameleonic-Ambience](https://plus.google.com/u/0/117867558830601601230/posts/LGHt9zzAPWp).

All _this_ version wants to achieve is colorize the Ambience theme -- both the GTK selection highlights and Metacity (and Unity) close buttons -- to whatever the _user_ wants, and then apply it.

Usage
-----

Presently, it's command-line only, just like the original. Use it like:

	./ambience-coloreon.py fab1ed
	
Where `fab1ed` is any hexadecimal encoded color you've tastefully picked out beforehand. 

I intend to provide a simple GUI utlity to make this less work. Let's see... `Quickly`?

Dependencies
------------

The script itself makes use of only standard Python modules, and ImageMagick, both of which should be installed on most Linux systems.

However, since the script concerns itself with the Ambience theme and assumes it to be installed system-wide, that too is a dependency.

