#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2005-2008 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-static \
                         --enable-libgdbm-compat")

def build():
    autotools.make("prefix=/usr")

def install():
    autotools.install("prefix=%s/usr" % get.installDIR())

    pisitools.dodoc("ChangeLog", "NEWS", "README")
