#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# You can use these as variables, they will replace GUI values before build.
# Package Name : keybinder
# Version : 0.3.0
# Summary : keybinder is a library for registering global keyboard shortcuts.

# If the project that you are tying to compile is in a sub directory in the 
# source archive, than you can define working directory. For example; 
# WorkDir="keybinder-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    autotools.configure("--disable-lua \
                         --disable-python")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")
# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("keybinder")
