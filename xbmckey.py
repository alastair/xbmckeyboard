#!/usr/bin/python

import ConfigParser
import os
import urllib2
import termios
import fcntl
import sys

config=ConfigParser.RawConfigParser()
BASE_KEY = 0xF100

alternates = {
  65362: 0x10E, # Up
  65364: 0x10F, # Down
  65361: 0x110, # left
  65363: 0x111 # right
}

def send_key(c):
	if c in alternates:
		tosend = alternates[c]	
	else:
		tosend = BASE_KEY + c
	host = config.get("xbmckey", "host")
	try:
		urllib2.urlopen("http://%s/xbmcCmds/xbmcHttp?command=SendKey(0x%X)" % (host, tosend))
	except urllib2.HTTPError, e:
		if e.code == 401:
			print "Unauthorised: is your user/pass set correctly?"
	except urllib2.URLError:
		print "Connection refused: is the host set correctly and running?"

def load():
	config.add_section("xbmckey")
	config.set("xbmckey", "host", "")
	config.set("xbmckey", "user", "")
	config.set("xbmckey", "pass", "")
	config.read(os.path.expanduser("~/.xbmckeyrc"))
	host = config.get("xbmckey", "host")
	username = config.get("xbmckey", "user")
	password = config.get("xbmckey", "pass")

	if host == "":
		return False

	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(realm='GoAhead',
	      uri='http://' + host + '/xbmcCmds/xbmcHttp',
	      user=username,
	      passwd=password)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)
	return True
