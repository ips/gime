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
from subprocess import Popen

if (len(sys.argv) > 1):
    name = sys.argv[1]
else:
    name = ''

command = "lzma -S .gime"

def compress(s):
    try:
        print "Compressing %s ...\n" %name
        compress = Popen(command+' '+s, shell=True)
        os.waitpid(compress.pid, 0)
        print "Done\n"
    except IndexError: 
            sys.stderr.write('Error: Wrong filename\n')

def uncompress(s):
    try:
        print "Decompressing %s ...\n" % name
        uncompress = Popen(command+' -d '+s, shell=True)
        os.waitpid(uncompress.pid, 0)
        print "Done\n"
    except IndexError: 
            sys.stderr.write('Error: Wrong filename\n')
if name:
    if name.endswith('.gime'):
        uncompress(name)
    else:
        compress(name)
else:
    sys.stderr.write("Error: Bad usage, please run \n\tgime-lzma imagename\n")
