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

if len(sys.argv) > 1:
    if len(sys.argv) >= 1:
        name = sys.argv[1]
    else:
        name = ''
    installer = sys.argv[4]
    size1 = sys.argv[2]
    size2 = sys.argv[3]
    if len(sys.argv)  == 6:
        fs = sys.argv[5]
    else:
        fs = "ext4"
else:
    help()

def help():
    print """Usage:
mkgime filename size xX installer [filesystem]\n
\tfilename      - GameImage file name (without .gime suffix)
\tsize          - Size of a GameImage, accepted 1G 2G 4G 8G and 16G
\txX            - Number of repeats of the size (ex. size = 512 mb, repeated 2, target size 1 gb)
\tinstaller     - full or releative path to the installer
\tfilesystem    - the filesystem to use (must be created with mkfs.filesystem!), if not specified forcing ext4"""
    exit(code=1)

def version_check():
    if os.path.exists('/usr/bin/wine'):
        command = "wine --version"
    else:
        print >>sys.stderr, "Please install wine"
        exit(code=1)

    opt = subprocess.Popen(command, shell=True, stderr=None, stdout=subprocess.PIPE).communicate()[0]

    if opt.find('1.0.1') > 0:
        if os.path.exists('/usr/bin/aptitude'):
            print >>sys.stderr, "Wine version in Your system is too old. Please update. Make sure the unstable Wine repository is on top in sources.list"
        else: 
            print >>sys.stderr, "Wine version in Your system is too old. Please update."
        exit(code=1)
    else:
        print "Wine version in Your system is ok."

def summary(n, i, s1, s2, fs):
    print """--------------------------------------
File uncompressed: %s
File compressed: %s.gime
Installer: %s
Size of uncompressed GameImage: %s x %s
Filesystem: %s
-------------------------------------
-> Proceeding""" % (n, n, i, s1, s2, fs)

if len(name) == 0 or name == "--help":
    help()
elif os.path.exists(name):
    print >>sys.stderr, "File exists!"
    exit(code=1)

version_check()

summary(name, installer, size1, size2, fs)

print "-> Creating %s with size %sx%s" % (name, size1, size2)
dd_command = "dd if=/dev/zero of=%s bs=%s count=%s" % (name, size1, size2)
dd = subprocess.call(dd_command, shell=True)
if dd < 0:
    print >>sys.stderr, "Error!", -dd
    exit(code=1)

print "-> Making new filesystem on %s - %s..." % (name, fs)

mkfs_path = "/sbin/mkfs.%s" % fs
if os.path.exists(mkfs_path):
    print "--> /sbin/mkfs.%s exists, using it..." % fs
    if fs.find('ext') > 0:
        ext = '-F '
    else:
        ext = ''
    mkfs_command = "%s %s%s" % (mkfs_path, ext, name)
    print mkfs_command

    mkfs = subprocess.call(mkfs_command, shell=True)
    if mkfs < 0:
        print >>sys.stderr, "--> Filesystem creation failed!", -mkfs
        exit(code=1)
    else:
        print "--> fs created"
else:
    print >>sys.stderr, "--> can't locate /sbin/mkfs.%s! you have to install package that contains tools for filesystem that you've chosen" % fs
    exit(code=1)

if os.path.exists('/usr/bin/sudo'):
    print "-> found sudo in /usr/bin/sudo, using it to mount"
    mntname = "%s-mnt" % name
    if os.path.exists(mntname) == "false":
       os.mkdir(mntname)
    mnt_cmd = "sudo mount -o rw,user,loop -t %s %s %s" % (fs, name, mntname)
    mnt = subprocess.call(mnt_cmd, shell=True)
    if mnt < 0:
        print >>sys.stderr, "--> Mounting failed!", -mnt
        exit(code=1)
    print "-> CHOWNing"
    user = os.geteuid()
    gid = os.getgid()
    os.chown(mntname, user, gid)
    print "-> Making new wine environment on %s... The winecfg window will appear, please configure all." % name
    home = os.getenv('PWD')
    wprefix = "%s/%s/wine-env" % (home, mntname)
    os.putenv('WINEPREFIX', wprefix)
    subprocess.Popen('winecfg', shell=True).communicate()[0]
    print "-> Installing game in image..."
    subprocess.Popen(['wine', installer], shell=True).communicate()[0]
    cp_cmd = "cp gime-basic-env/__run__.sh %s/%s" % (home, mntname)
    subprocess.Popen(cp_cmd, shell=True).communicate()[0]

    print """Now change the initial __run__.sh script to run your game. You have time 
to configure your game and apply patches. After that unmount this dir.
The mounted image directory is imagename-mnt. To unmount type sudo unmount imagename-mnt,
if you want to prepare the  image for distribution or just make it smaller, 
type: ./gime-lzma imagename.  Mounting again is simple. Type ./gimemount imagename 
- if you used gime-lzma tool before, or you downloaded image from internet it will
be decompressed first. This can take an long time, but is 2x faster than 
compression ( ./gime-lzma )."""

