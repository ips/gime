#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#   Copyright 2009  ExeGames.PL & Serenity.org.pl
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

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = ''

if len(name) >= 1:
    current_dir = os.getenv('PWD')
    mntname = "%s-mnt" % name 
    mnt_dir = "%s/%s" % (current_dir, mntname)
    if len(sys.argv) >= 3:
        fs = sys.argv[2]
    else:
        fs = "ext4"

def helpmsg():
    print """Usage:
./gime-mount imagename [filesystem]
    imagename   - name of image (without .gime suffix)
    filesystem  - optional, if image have an custom filesystem"""

def mounter():
    mnt_cmd = "sudo mount -o loop -t %s %s %s" % (fs, name, mntname)
    mount = subprocess.Popen(mnt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    mnt_stdout = mnt.communicate()[0]
    if mnt_stdout:
        print >>sys.stderr, "--> Mounting failed!", -mnt_stdout 
        sys.exit(1)
    else: 
        print "Image mounted..."
    user = os.getenv('LOGNAME')
    chown_cmd = "sudo chown -R %s %s" % (user, to_mount)
    chown = subprocess.Popen(chmod_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    chown_stdout = chmod.communicate()[0]
    if chown_stdout:
        print >>sys.stderr, "--> CHMODing failed!", -chown_stdout
        sys.exit(1)
    else:
        print "And CHOWNed."
    print "Done!" 


if len(name) == 0 or name.find('--help'):
    helpmsg()
    sys.exit(0)

if name.endswith('.gime') and os.path.exists(mnt_dir):
    print "-> Found compressed image."
    print "Decompressing %s ..." % name
    uncmd = "%s -d %s" % (command, s)
    uncompress = subprocess.Popen(uncmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
    print "Done"
    name.rstrip('.gime')
    print "Image nad directory: Found", name
    mounter()
elif name and os.path.exists(mnt_dir):
    print "Image nad directory: Found"
    mounter()
else:
    print >>sys.stderr, "Error! Can't find image or mount directory!"
