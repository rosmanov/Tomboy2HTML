#!/usr/bin/env python2
# Copyright (C) 2011 - Ruslan Osmanov <rrosmanov@gmail.com>
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
# 
##
# @file tomboy2html.py
# @brief Export all Tomboy notes in XHTML/HTML file(s)
# @author Ruslan Osmanov
# @version 1.3
# @date 08.02.2011
# @details xsltproc utility required
# @copyright Copyright (C) 2011-2012 Ruslan Osmanov <rrosmanov at gmail dot com>

import dbus, dbus.glib
try:
    import gobject
except ImportError:
    # gobject functions are moved to dbus.glib in this Python version
    pass
import os, sys, getopt
import re

def usage():
    print __file__ + " [OPTIONS]"
    print """Options:
-h, --help      Display help
-p, --prefix    Optional. Output filename prefix. Default: notes
-x, --xhtml     Optional. Generate XHTML file also. Default: off 
-s, --xsl       Optional. XSL for XML-HTML conversion. Default: tomboy-notes.xsl 
-d, --debug     Optional. Debug mode. Default: off 
"""

def main(argv):
    debug_mode = False
    prefix = 'notes'
    xhtml = False
    xsl_filename = os.path.dirname(__file__) + '/tomboy-notes.xsl'

    # Get CLI options
    try:
        opts, args = getopt.getopt(argv[1:], "s:p:xhd", 
                ("xsl=", "prefix=", "debug", "xhtml", "help"))

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

        elif o in ("-p", "--prefix"):
            prefix = os.path.expanduser(a)

        elif o in ("-s", "--xsl"):
            xsl_filename = os.path.expanduser(a)

    xhtml_filename = prefix + '.xhtml'
    html_filename = prefix + '.html'
    if False == os.path.exists(xsl_filename):
        print "XSL file '"+xsl_filename+"' doesn't exist"
        sys.exit(2)

    if debug_mode:
        print "xhtml =", xhtml_filename, "\nhtml =", html_filename
        print "\nxsl =", xsl_filename

    # Access the Tomboy remote control interface
    bus = dbus.SessionBus()
    obj = bus.get_object("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
    tomboy = dbus.Interface(obj, "org.gnome.Tomboy.RemoteControl")

    # Get note URIs
    all_notes = tomboy.ListAllNotes()

    # Write each note XML to the XHTML file
    f = open(xhtml_filename, "w")
    f.write('<?xml version="1.0" encoding="utf-8"?>' + 
            '<?xml-stylesheet type="text/xsl" href="' +xsl_filename+'"?>'
            '<notes>')
    for n in all_notes:
        if (debug_mode):
            print "NOTE '"+n+"'"
        xml = re.sub(r'<\?xml[^<]*\?>', '', tomboy.GetNoteCompleteXml(n))
        xml = re.sub(r'\&\#x?.*\;', '', xml)
        f.write(unicode(xml).encode("utf-8"))

    f.write('</notes>')
    f.close()

    # Generate HTML
    cmd = "xsltproc -o '%(html)s' '%(xsl)s' '%(xhtml)s'" % \
            {'html': html_filename.replace("'", "\\'"), 
                    'xsl': xsl_filename, 
                    'xhtml': xhtml_filename}
    if debug_mode:
        print cmd
    os.system(cmd)

    if xhtml == False:
        os.unlink(xhtml_filename)

if __name__ == "__main__":
    main(sys.argv)
