#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#   Copyright 2009 ExeGames.PL & Serenity.org.pl
#   license = GPLv3 
#   version =
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess 

if (len(sys.argv) > 1):
    name = sys.argv[1]
else:
    name = ''

def help():
    print """Usage:
mkgime filename size xX installer [filesystem]\n
\tfilename      - GameImage™ file name (without .gime suffix)
\tsize          - Size of a GameImage™, accepted 1G 2G 4G 8G and 16G
\txX            - Number of repeats of the size (ex. size = 512 mb, repeated 2, target size 1 gb)
\tinstaller     - full or releative path to the installer
\tfilesystem    - the filesystem to use (must be created with mkfs.filesystem!), if not specified forcing ext4\n"""

def debian_check():

    command = "wine --version"
    opt = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    optdata = opt.communicate() [0]

    if optdata.find('1.0.1') > 0:
        print "The Wine version in your repository is too old. Please update. Make sure the unstable Wine repository is on top in sources.list\n"

    else:
        print "The Wine version in your repository is ok.\n"

if len(name) == 0 or name == "--help":
    help()
elif os.path.exists(name):
    print "File exists!\n"

if os.path.exists('/usr/bin/aptitude'):
    debian_check()



