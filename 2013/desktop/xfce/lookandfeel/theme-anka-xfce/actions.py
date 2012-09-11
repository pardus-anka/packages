#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools

# You can use these as variables, they will replace GUI values before build.
# Package Name : theme-anka-xfce
# Version : 1
# Summary : A special window theme for Xfce on Pardus

# If the project that you are tying to compile is in a sub directory in the 
# source archive, than you can define working directory. For example; 
# WorkDir="theme-anka-xfce-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    
    pisitools.dodir("/usr/share/themes/Anka-Xfce")


def install():

    pisitools.insinto("/usr/share/themes/Anka-Xfce/", "xfwm4")
    pisitools.insinto("/usr/share/themes/Anka-Xfce/", "gtk-2.0") 