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
#   (at  option) any later version.
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
if len(sys.argv) >= 5:
    installer = sys.argv[4]
    size1 = sys.argv[2]
    size2 = sys.argv[3]
    if len(sys.argv)  == 6:
        fs = sys.argv[5]
    else:
        fs = "ext4"
if len(name) > 0 and len(sys.argv) >= 5:
    mntname = "%s-mnt" % name
    currentdir = os.getenv('PWD')
    to_mount = "%s/%s" % (currentdir, mntname)
    imgpath = "%s/%s" % (currentdir, name)

def helpmsg():
    print """Usage:
mkgime filename size xX installer [filesystem]\n
\tfilename      - GameImage file name (without .gime suffix)
\tsize          - Size of a GameImage, accepted 1G 2G 4G 8G and 16G
\txX            - Number of repeats of the size (ex. size = 512 mb, repeated 2, target size 1 gb)
\tinstaller     - full or releative path to the installer
\tfilesystem    - the filesystem to use (must be created with mkfs.filesystem!), if not specified forcing ext4"""
    
def failed():
    if os.path.exists(imgpath):
        os.remove(imgpath)
    sys.exit(1)

def version_check():
    if os.path.exists('/usr/bin/wine'):
        command = "wine --version"
    else:
        print >>sys.stderr, "Please install wine"
        failed()

    opt = subprocess.Popen(command, shell=True, stderr=None, stdout=subprocess.PIPE)
    opt_stdout = opt.communicate()[0]

    if opt_stdout.find('1.0.1') > 0:
        if os.path.exists('/usr/bin/aptitude'):
            print >>sys.stderr, "Wine version in Your system is too old. Please update. Make sure the unstable Wine repository is on top in sources.list"
        else: 
            print >>sys.stderr, "Wine version in Your system is too old. Please update."
        failed()
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
    helpmsg()
    sys.exit(0)
elif os.path.exists(name):
    print >>sys.stderr, "File exists!"
    sys.exit(1)
version_check()
summary(name, installer, size1, size2, fs)
print "-> Creating %s with size %sx%s" % (name, size1, size2)
dd_command = "dd if=/dev/zero of=%s bs=%s count=%s" % (name, size1, size2)
dd = subprocess.call(dd_command, shell=True)
if dd < 0:
    print >>sys.stderr, "Error!", -dd
    failed()
print "-> Making new filesystem on %s - %s..." % (name, fs)
mkfs_path = "/sbin/mkfs.%s" % fs
if os.path.exists(mkfs_path):
    print "--> /sbin/mkfs.%s exists, using it..." % fs
    if fs.find('ext') > 0:
        fs_mod = '-F '
    elif fs == "xfs":
        xfs_check = subprocess.Popen("mkfs.xfs -V", stdout=subprocess.PIPE, shell=True).communicate()[0]
        if xfs_check.find('3.0'):
            fs_info = os.stat(imgpath).st_size
            print fs_info

            fs_mod = "-d size=%s " % fs_info
        else:
            fs_mod = ''
    else:
        fs_mod = ''
    mkfs_command = "%s %s%s" % (mkfs_path, fs_mod, imgpath)
    mkfs = subprocess.call(mkfs_command, shell=True)
    if mkfs < 0:
        print >>sys.stderr, "--> Filesystem creation failed!", -mkfs
        failed()
    else:
        print "--> fs created"
else:
    print >>sys.stderr, "--> can't locate /sbin/mkfs.%s! you have to install package that contains tools for filesystem that you've chosen" % fs
    failed()
if os.path.exists('/usr/bin/sudo'):
    print "-> found sudo in /usr/bin/sudo, using it to mount"
    if os.path.exists(to_mount):
        print "Directory %s exists: OK" % to_mount
    else:
        os.mkdir(to_mount)
    mnt_cmd = "sudo mount -o rw,user,loop -t %s %s %s" % (fs, name, mntname)
    mnt = subprocess.Popen(mnt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    mnt_stdout = mnt.communicate()[0]
    if mnt_stdout:
        print >>sys.stderr, "--> Mounting failed!", -mnt_stdout 
        failed()
    print "-> CHOWNing"
    user = os.getenv('LOGNAME')
    chown_cmd = "sudo chown -R %s %s" % (user, to_mount)
    chown = subprocess.Popen(chown_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    chown_stdout = chown.communicate()[0]
    if chown_stdout:
        print >>sys.stderr, "--> CHONing failed!", -chown_stdout 
        failed()
    print "-> Making new wine environment on %s... The winecfg window will appear, please configure all." % name
    currentdir = os.getenv('PWD')
    wprefix = "%s/%s/wine-env" % (currentdir, mntname)
    os.putenv('WINEPREFIX', wprefix)
    subprocess.Popen('winecfg', shell=True).communicate()[0]
    print "-> Installing game in image..."
    wcmd = "wine %s" % installer
    subprocess.Popen(wcmd, shell=True).communicate()[0]
    cp_cmd = "cp %s/gime-basic-env/__run__.sh %s/%s" % (currentdir, currentdir, mntname)
    subprocess.Popen(cp_cmd, shell=True).communicate()[0]
    print """--------------------------------------
Now change initial __run__.sh script to run  game. It's time 
to configure Your game and apply patches. After that Youve to unmount this dir, 
mounted image directory is imagename-mnt. To unmount type sudo unmount imagename-mnt.
If you want to make this image portable or just make it smaller, type: 
./gime-lzma imagename.  

Mounting again is simple, type 
./gime-mount imagename 

If you used gime-lzma tool before, or you downloaded image from internet it will
be decompressed first. This can take an long time, but is 2x faster than 
compression ( ./gime-lzma ).
--------------------------------------"""

