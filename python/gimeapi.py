# -*- encoding: utf-8 -*-
# This program is free software. You can redistribute it under terms of GNU General Public License 3.
# This is a GIME API, do not run it.
import os
import shutil
import logging
import logging.handlers

debug = False;
logfile = os.environ['HOME'] + "/.gime-api-log"

if debug:
#	logging.basicConfig(filename=logfile,level=logging.DEBUG,)
	logging.basicConfig(level=logging.DEBUG,)
else:
	logging.basicConfig(level=logging.WARNING,)

log = logging.getLogger("gime-api")

class GIMEAPI:
	"""A simple GIME Python API for creating and managing images
	   (c) 2009 by ExeGames.PL & Serenity.org.pl"""
	cdir = os.getcwdu()
	log.debug('Current dir is (unicode): %s', cdir)

	def CreateImage(filename, filesystem="ext4"):
		"""Creates an GIME Image.
		   @returns: True if successful, error code for HandleError if fails."""
		
