#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

import os

default_flags = "-g -U_FORTIFY_SOURCE -fno-strict-aliasing -fomit-frame-pointer -mno-tls-direct-seg-refs"
sysflags = "-mtune=generic -march=x86-64 -O3" if get.ARCH() == "x86_64" else "-mtune=atom -march=i686 -O2 -pipe"

def set_variables():
    shelltools.export("LANGUAGE","C")
    shelltools.export("LANG","C")
    shelltools.export("LC_ALL","C")

    if get.buildTYPE() == "emul32":
        shelltools.export("CC", "gcc -m32")
        shelltools.export("CXX", "g++ -m32")

    shelltools.export("CFLAGS", "%s %s" % (default_flags, sysflags))
    shelltools.export("CXXFLAGS", "%s %s" % (default_flags, sysflags))

def removePardusSection(_dir):
    for root, dirs, files in os.walk(_dir):
        for name in files:
            # FIXME: should we do this only on nonshared or all ?
            # if ("crt" in name and name.endswith(".o")) or name.endswith("nonshared.a"):
            if ("crt" in name and name.endswith(".o")) or name.endswith(".a"):
                i = os.path.join(root, name)
                shelltools.system('objcopy -R ".comment.PARDUS.OPTs" -R ".note.gnu.build-id" %s' % i)

def setup():
    set_variables()
    shelltools.makedirs("build")
    shelltools.cd("build")

    options = "--prefix=/usr \
               --enable-add-ons=nptl,libidn \
               --enable-obsolete-rpc \
               --enable-kernel=3.2.5 \
               --enable-bind-now \
               --disable-profile \
               --enable-stackguard-randomization \
               --enable-multi-arch \
               --without-cvs \
               --without-gd \
               --without-selinux \
               --with-tls \
               --with-__thread"

    if get.buildTYPE() == "emul32":
        options += " --libdir=/usr/lib32 \
                     --libexecdir=/usr/lib32/misc \
                     --build=i686-pc-linux-gnu"
    else:
        options += " --libdir=/usr/lib \
                     --libexecdir=/usr/lib/misc \
                     --build=%s" % get.HOST()

    shelltools.system("../configure %s" % options)

def build():
    set_variables()
    shelltools.cd("build")
    autotools.make()

def install():
    set_variables()
    pisitools.dodoc("BUGS", "ChangeLog*", "CONFORMANCE", "NAMESPACE", "NEWS", "PROJECTS", "README*", "LICENSES")
    shelltools.cd("build")

    libdir = "lib" if get.buildTYPE() != "emul32" else "lib32"
    installdir = get.installDIR() if get.buildTYPE() != "emul32" else get.installDIR() + "/emul32"

    autotools.rawInstall("install_root=%s" % installdir)

    if get.buildTYPE() != "emul32":
        autotools.rawInstall("install_root=%s localedata/install-locales" % installdir)

    pisitools.dosym("libbsd-compat.a", "/usr/%s/libbsd.a" % libdir)

    if get.buildTYPE() == "emul32":
        pisitools.dosym("../lib32/ld-linux.so.2", "/lib/ld-linux.so.2")

    removePardusSection("%s/usr/%s/" % (installdir, libdir))

    # It previously has 0755 perms which was killing things
    shelltools.chmod("%s/usr/%s/misc/pt_chown" % (installdir, libdir), 04711)

    if shelltools.isFile("%s/etc/ld.so.cache" % installdir):
        pisitools.remove("/etc/ld.so.cache")

    # Prevent overwriting of the /etc/localtime symlink
    if shelltools.isFile("%s/etc/localtime" % installdir):
        pisitools.remove("/etc/localtime")

    # Nscd needs this to work
    pisitools.dodir("/var/run/nscd")
    pisitools.dodir("/var/db/nscd")

    # remove zoneinfo files since they are coming from timezone packages
    # we disable timezone build with a patch, keeping these lines for easier maintenance
    if shelltools.isDirectory("%s/usr/share/zoneinfo" % installdir):
        pisitools.removeDir("/usr/share/zoneinfo")

    for i in ["zdump", "zic"]:
        if shelltools.isFile("%s/usr/sbin/%s" % (installdir, i)):
            shelltools.unlink("%s/usr/sbin/%s" % (installdir, i))

    if get.buildTYPE() == "emul32":
        shelltools.move("%s/lib32" % installdir,"%s" % get.installDIR())
        shelltools.move("%s/usr/lib32/*" % installdir,"%s/usr/lib32" % get.installDIR())
        shelltools.move("%s/usr/include/gnu/stubs-32.h" % installdir,"%s/usr/include/" % get.installDIR())
        pisitools.dobin("%s/usr/bin/lddlibc4" % installdir)
        pisitools.dosym("/usr/lib/locale","/usr/lib32/locale")
        pisitools.removeDir("emul32")
