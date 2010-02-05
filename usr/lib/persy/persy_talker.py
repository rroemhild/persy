#!/usr/bin/env python
# -*- coding: utf-8 -*-

#License
#=======
#persy is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the Free
#Software Foundation, either version 2 of the License, or (at your option) any
#later version.

#persy is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with persy; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

try:
	import gettext
	#localizations
	LOCALEDIR='/usr/lib/persy/locale'
	#init the localisation
	gettext.install("messages", LOCALEDIR)
except Exception as e:
	print "I have problems initializing the translations (gettext). Will use plain english instead"
	print str(e)

	#check if the _ function is initialized, if not, do a fallback!
	if not _:
		def _(msg):
			"""fallback-function if the original function did not initialize propperly"""
			return msg


try:
	import sys
	import os
	import pynotify
	import gtk
	import logging , logging.handlers
except ImportError as e:
	print _("You do not have all the dependencies:")
	print str(e)
	sys.exit(1)
except Exception as e:
	print _("An error occured when initialising one of the dependencies!")
	print str(e)
	sys.exit(1)

__author__ = "Dennis Schwertel"
__copyright__ = "Copyright (C) 2009, 2010 Dennis Schwertel"


class Talker:
	'''logging, notifications and communications with the outside!
if the critical or warning function is called, the Talker goes into an "error occured" mode:
The statusicon will not change to any other state until this errorstate is reseted.
'''
	def __init__(self, config, verbose=False):
		self.statusIcon = None
		self.config = config
		#init logging 
		self.log = logging.getLogger("")
		os.popen("touch %s"%self.config.getAttribute('LOGFILE'))
		hdlr = logging.handlers.RotatingFileHandler(self.config.getAttribute('LOGFILE'), "a", 1000000, 3)
		fmt = logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", "%x %X")
		hdlr.setFormatter(fmt)
		self.log.addHandler(hdlr)
		self.verbose = verbose

		#init notify
		self.notifyid = "Persy"
		try:
			pynotify.init(self.notifyid)
		except Exception as e:
			self.log.warn(str(e))

		self.resetError()

	def notify(self, text, icon):
		pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon, 64, 64)
		n = pynotify.Notification(self.notifyid, text)
		n.set_icon_from_pixbuf(pixbuf)
		n.show()

	def setStatusIcon(self, icon):
		'''sets the status icon'''
		self.statusIcon = icon

	def setStart(self):
		'''can be called to tell "everybody" when persy is started'''
		if self.statusIcon:
			self.statusIcon.set_from_file(self.config.getAttribute('ICON_OK'))#from_stock(gtk.STOCK_HOME)
		try:
			self.notify(_('starting Persy'), self.config.getAttribute('ICON_OK'))
		except Exception as e:
			self.log.warn(str(e))

	def setStop(self):
		'''can be called to tell "everybody" when persy is stopped'''
		if self.statusIcon:
			self.statusIcon.set_from_file(self.config.getAttribute('ICON_IDLE'))#from_stock(gtk.STOCK_HOME)
		try:
			self.notify(_('stopping Persy'), self.config.getAttribute('ICON_IDLE'))
		except Exception as e:
			self.log.warn(str(e))

	def resetError(self):
		'''resets the error state'''
		self.error = False

	def untracked_changes(self, uc):
		'''sets or unsets the untracked_changes status -> sets the status icon'''
		if not self.error:
			if uc:
				if self.statusIcon:
					self.statusIcon.set_from_file(self.config.getAttribute('ICON_UNTRACKED'))
			else:
				if self.statusIcon:
					self.statusIcon.set_from_file(self.config.getAttribute('ICON_OK'))

	def unsynced_changes(self, uc):
		'''sets or unsets the unsynced_changes status -> sets the status icon'''
		if not self.error:
			if uc:
				if self.statusIcon:
					self.statusIcon.set_from_file(self.config.getAttribute('ICON_UNSYNCED'))
			else:
				if self.statusIcon:
					self.statusIcon.set_from_file(self.config.getAttribute('ICON_OK'))

	def setLevel(self, lvl):
		'''set the logging level. see logging.INFO = false,logging.DEBUG = true... for more information'''
		self.log.setLevel((logging.INFO,logging.DEBUG)[lvl])

	def debug(self, msg, verbose=None):
		'''logs a debug message'''
		self.log.debug(msg)
		if verbose == True or (verbose == None and self.verbose):
			print msg

	def info(self, msg, verbose=None):
		'''logs a info message'''
		self.log.info(msg)
		if verbose == True or (verbose == None and self.verbose):
			print msg

	def warn(self, msg, verbose=None):
		''' logs a warning message, changes the status icon, fires a notification and sets the error state'''
		self.error = True
		self.log.warn(msg)
		if verbose == True or (verbose == None and self.verbose):
			print msg
		if self.statusIcon:
			self.statusIcon.set_from_file(self.config.getAttribute('ICON_WARN'))#from_stock(gtk.STOCK_HOME)
		try:
			self.notify(msg, self.config.getAttribute('ICON_WARN'))
		except Exception as e:
			pass #self.log.warn(str(e))

	def critical(self, msg, verbose=None):
		''' logs a critical message, changes the status icon, fires a notification and sets the error state'''
		self.error = True
		self.log.critical(msg)
		if verbose == True or (verbose == None and self.verbose):
			print msg
		if self.statusIcon:
			self.statusIcon.set_from_file(self.config.getAttribute('ICON_ERROR'))#from_stock(gtk.STOCK_HOME)
		try:
			self.notify(msg, self.config.getAttribute('ICON_ERROR'))
		except Exception as e:
			pass #self.log.warn(str(e))





