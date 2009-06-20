#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#   Copyright 2009 Marcin Karpezo <sirmacik at gmail dot com>
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
from subprocess import Popen

if (len(sys.argv) > 1):
    name = sys.argv[1]
else:
    name = ''

def help():
    print """Usage:
mkgime filename size xX installer [filesystem]\n
\tfilename - GameImage™ file name (without .gime suffix)
\tsize - Size of a GameImage™, accepted 1G 2G 4G 8G and 16G
\txX - Number of repeats of the size (ex. size = 512 mb, repeated 2, target size 1 gb)
\tinstaller - full or releative path to the installer
\tfilesystem - the filesystem to use \(must be created with mkfs.filesystem!\), if not specified forcing ext4\n"""

def summary():
    
help()
