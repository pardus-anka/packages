
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import kde4
from pisi.actionsapi import pkgconfig

WorkDir = "%s-%s.src" % (get.srcNAME(), get.srcVERSION())
libdir = "/usr/lib/llvm"

def setup():
    if not shelltools.isDirectory("tools/clang"):
        shelltools.move("tools/clang-%s.src" % get.srcVERSION(), "tools/clang")

    pisitools.dosed("utils/llvm-build/llvm-build", "python", "python2.7")
    pisitools.dosed("bindings/ocaml/Makefile.ocaml", '\$\(PROJ_libdir\)', "/usr/lib/llvm")
    pisitools.dosed("Makefile.config.in", "\$\(PROJ_prefix\)/etc/llvm", "/etc/llvm")
    pisitools.dosed("Makefile.config.in", "\$\(PROJ_prefix\)/lib", "$(PROJ_prefix)/lib/llvm")
    pisitools.dosed("Makefile.config.in", "\$\(PROJ_prefix\)/docs/llvm", "$(PROJ_prefix)/share/doc/llvm")
    pisitools.dosed("tools/llvm-config/llvm-config.cpp", '(ActiveLibDir\s=\sActivePrefix\s\+\s\"\/lib)(.*)', r'\1/llvm\2')
    pisitools.dosed("autoconf/configure.ac", '\LLVM_LIBDIR="\$\{prefix\}/lib"', 'LLVM_LIBDIR="${prefix}/lib/llvm"')

    #autotools.configure()
    
    pisitools.dosed("Makefile.rules", "\$\(RPATH\)\s-Wl,\$\(ExmplDir\)\s\$\(DynamicFlag\)", "$(DynamicFlag)")
    pisitools.dosed("Makefile.rules", "\$\(RPATH\)\s-Wl,\$\(ToolDir\)\s\$\(DynamicFlag\)", "$(DynamicFlag)")
    
    #shelltools.export("CPPFLAGS",get.CXXFLAGS())
    shelltools.export("CPPFLAGS","%s %s" % (get.CXXFLAGS(),pkgconfig.getLibraryCFLAGS("libffi")))
    
    shelltools.export("CC",get.CC())
    shelltools.export("CXX",get.CXX())
    
    pic_option = "enable" if get.ARCH() == "x86_64" else "disable"
    
    options = "--libdir=%s \
               --datadir=/usr/share/llvm \
               --sysconfdir=/etc \
               --disable-expensive-checks \
               --disable-assertions \
               --disable-debug-runtime \
               --enable-optimized \
               --enable-debug-symbols \
               --enable-jit \
               --enable-threads \
               --%s-pic \
               --enable-shared \
               --enable-targets=host \
               --enable-bindings=all \
               --with-binutils-include=/usr/include \
               --enable-libffi \
               " % (libdir, pic_option)

    if get.buildTYPE() == "emul32":
        options += " --prefix=/emul32 \
                     --libdir=/usr/lib32"

        #shelltools.export("CFLAGS", "%s -m32" % get.CFLAGS())
        shelltools.export("CC", "%s -m32" % get.CC())
        shelltools.export("CXX", "%s -m32" % get.CXX())

    
    autotools.configure(options)


#def check():
#    autotools.make("check")
#    autotools.make("-C tools/clang test")

def build():
    autotools.make("REQUIRES_RTTI=1")

def install():
    if get.buildTYPE() == "emul32":

        autotools.rawInstall("DESTDIR=%s \
                              PROJ_etcdir=/etc/llvm \
                              PROJ_libdir=/usr/lib32/llvm \
                              PROJ_docsdir=/%s/llvm"
                              % (get.installDIR(),  get.docDIR()))
        pisitools.removeDir("/emul32")
        # Remove executable bit from static libs
        shelltools.chmod("%s/usr/lib32/*/*.a" % get.installDIR(), 0644)
        return
    else:
        autotools.rawInstall("DESTDIR=%s \
                              PROJ_etcdir=/etc/llvm \
                              PROJ_libdir=%s \
                              PROJ_docsdir=/%s/llvm"
                              % (get.installDIR(), libdir, get.docDIR()))


    # Install static analyzers which aren't installed by default
    for exe in ("scan-build", "scan-view"):
        pisitools.insinto("/usr/lib/clang-analyzer/%s" % exe, "tools/clang/tools/%s/%s" % (exe, exe))
        pisitools.dosym("/usr/lib/clang-analyzer/%s/%s" % (exe, exe), "/usr/bin/%s" % exe)

    pisitools.dodir("/etc/ld.so.conf.d")
    shelltools.echo("%s/etc/ld.so.conf.d/51-llvm.conf" % get.installDIR(), "/usr/lib/llvm")

    # Remove executable bit from static libs
    shelltools.chmod("%s/usr/lib/*/*.a" % get.installDIR(), 0644)

    # Symlink the gold plugin where clang expects it
    pisitools.dosym("llvm/LLVMgold.so", "/usr/lib/LLVMgold.so")

    # Remove example file
    pisitools.remove("/usr/lib/llvm/*LLVMHello.*")

    pisitools.remove("/usr/share/doc/llvm/*.tar.gz")
    pisitools.remove("/usr/share/doc/llvm/ocamldoc/html/*.tar.gz")
    pisitools.removeDir("/usr/share/doc/llvm/ps")

    # Install vim syntax files for .ll and .td files
    # llvm.vim additional file add ftdetct vim file to detect .ll and .td as llvm files
    pisitools.insinto("/usr/share/vim/vimfiles/syntax", "utils/vim/*.vim")

    # Install kate syntax file
    pisitools.insinto("%s/katepart/syntax" % kde4.appsdir, "utils/kate/*.xml")

    pisitools.dodoc("CREDITS.TXT", "LICENSE.TXT", "README.txt")

 
