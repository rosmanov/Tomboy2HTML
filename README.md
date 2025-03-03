# Tomboy2HTML

Utility to export Tomboy notes to XHTML/HTML file(s).

## FILES

### tomboy2html.py

Python script for use in CLI.

### tomboy-notes.xsl

XSL file to generate HTML file from XML content.

### OPTIONS

```
-h, --help          Display help
-p, --prefix        Optional. Output filename prefix. Default: notes
-x, --xhtml         Optional. Generate XHTML file also. Default: off 
-s, --xsl           Optional. XSL for XML-HTML conversion. Default: tomboy-notes.xsl 
-d, --debug         Optional. Debug mode. Default: off 
```

### EXAMPLE

```
./tomboy2html.py -p "all_notes"
```

Generates `all_notes.html` in the current directory.

```
./tomboy2html.py --xhtml --prefix="/tmp/all_notes"
```

Generates files `/tmp/all_notes.xhtml` and `/tmp/all_notes.html`.

TROUBLESHOOTING
===============

If you encounter the following error:

```
ERROR: Dependency "dbus-1" not found, tried pkgconfig and cmake
```

Install the `dbus-devel` package (or equivalent) for your distribution.

If you encounter the following error:

```
ERROR: Dependency "glib-2.0" not found, tried pkgconfig and cmake
```

Install the `glib2-devel` package (or equivalent) for your distribution.
