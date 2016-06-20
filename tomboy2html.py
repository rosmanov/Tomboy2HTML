#!/usr/bin/env python2
# Exports all Tomboy notes in XHTML/HTML file(s)
# Note, xsltproc utility required
#
# Copyright (C) 2011-2016 - Ruslan Osmanov <rrosmanov@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# See <http://www.gnu.org/licenses/>

import dbus, dbus.glib
try:
    import gobject
except ImportError:
    # gobject functions are moved to dbus.glib in this Python version
    pass
import os, sys, getopt, subprocess
import re

def usage():
    print """Usage: %(file)s [OPTIONS]

OPTIONS
-------
-h, --help      Display help
-p, --prefix    Optional. Output path prefix. Default: notes
-x, --xhtml     Optional. Generate XHTML file also. Default: off
-s, --xsl       Optional. XSL for XML-HTML conversion. Default: tomboy-notes.xsl
-d, --debug     Optional. Debug mode. Default: off
-m, --multiple  Optional. Produce multiple files.

EXAMPLE
-------
Generates an HTML file for each note:
%(file)s -m -p /path/to/directory/""" % { "file": __file__ }


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def generate_html(html_filename, xsl_filename, xhtml_filename, debug_mode=False):
    rc = 0

    try:
        cmd = "xsltproc -o %(html)s %(xsl)s %(xhtml)s" % \
                {"html": shellquote(html_filename),
                        "xsl": shellquote(xsl_filename),
                        "xhtml": shellquote(xhtml_filename)}
        if debug_mode:
            print "Running %s" % cmd
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            print >>sys.stderr, "xsltproc failed, rc: ", rc
    except OSError as e:
        rc = 1
        print >>sys.stderr, "Execution failed:", e
    except:
        print >>sys.stderr, "Unexpected error:", sys.exc_info()[0]
        raise
        rc = 1;
    return rc


def save_note(tomboy, n, f, debug = False):
    if (debug):
        print "NOTE '", n, "'"
    xml = re.sub(r'<\?xml[^<]*\?>', '', tomboy.GetNoteCompleteXml(n))
    xml = re.sub(r'\&\#x?.*\;', '', xml)
    f.write(unicode(xml).encode("utf-8"))


def write_note_header(f, xsl_filename):
    f.write('<?xml version="1.0" encoding="utf-8"?>' +
            '<?xml-stylesheet type="text/xsl" href="' + xsl_filename + '"?>'
            '<notes>')


def write_note_bottom(f):
    f.write('</notes>')


def main(argv):
    multiple = False
    debug_mode = False
    prefix = 'notes'
    xhtml = False
    xsl_filename = os.path.dirname(__file__) + '/tomboy-notes.xsl'

    # Get CLI options
    try:
        opts, args = getopt.getopt(argv[1:], "s:p:xhdm",
                ("xsl=", "prefix=", "debug", "xhtml", "help", "multiple"))

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Save CLI options
    for o, a in opts:
        if o in ('-h', '--help'):
            usage();
            sys.exit();

        elif o in ('-x', '--xhtml'):
            xhtml = True

        elif o in ('-d', '--debug'):
            debug_mode = True

        elif o in ('-m', '--multiple'):
            multiple = True

        elif o in ("-p", "--prefix"):
            prefix = os.path.expanduser(a)

        elif o in ("-s", "--xsl"):
            xsl_filename = os.path.expanduser(a)

    if False == os.path.exists(xsl_filename):
        print "XSL file '", xsl_filename, "' doesn't exist"
        sys.exit(2)

    # Access the Tomboy remote control interface
    bus = dbus.SessionBus()
    obj = bus.get_object("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
    tomboy = dbus.Interface(obj, "org.gnome.Tomboy.RemoteControl")

    # Get note URIs
    all_notes = tomboy.ListAllNotes()

    if multiple == False:
        xhtml_filename = prefix + '.xhtml'
        html_filename = prefix + '.html'

        f = open(xhtml_filename, "w")
        write_note_header(f, xsl_filename)

        for n in all_notes:
            save_note(tomboy, n, f, debug_mode)

        write_note_bottom(f)
        f.close()
        generate_html(html_filename, xsl_filename, xhtml_filename, debug_mode);

        if xhtml == False:
            os.unlink(xhtml_filename)
    else:
        for n in all_notes:
            title = tomboy.GetNoteTitle(n)
            xhtml_filename = prefix + title + '.xhtml'
            html_filename = prefix + title +'.html'

            if debug_mode:
                print "open(%s)" % xhtml_filename
            f = open(xhtml_filename, "w")
            write_note_header(f, xsl_filename)
            save_note(tomboy, n, f, debug_mode)
            write_note_bottom(f)
            f.close()

            rc = generate_html(html_filename, xsl_filename, xhtml_filename, debug_mode);
            if rc != 0:
                print >>sys.stderr, "generate_html(%s, %s, %s) failed" \
                        [html_filename, xsl_filename, xhtml_filename]
                break
            if xhtml == False:
                os.unlink(xhtml_filename)

if __name__ == "__main__":
    main(sys.argv)
