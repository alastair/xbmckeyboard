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
  '\x7f' : 0xF108, # Backspace
  '\n': 0x100, # Select
#  '': 0x10E, # Up
#  '': 0x10F # Down
}

def send_key(c):
	if c in alternates:
		tosend = alternates[c]	
	else:
		tosend = BASE_KEY + ord(c)
	host = config.get("xbmckey", "host")
	urllib2.urlopen("http://%s/xbmcCmds/xbmcHttp?command=SendKey(0x%X)" % (host, tosend))

def main():
	config.read(os.path.expanduser("~/.xbmckeyrc"))
	host = config.get("xbmckey", "host")
	username = config.get("xbmckey", "user")
	password = config.get("xbmckey", "pass")

	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(realm='GoAhead',
	      uri='http://' + host + '/xbmcCmds/xbmcHttp',
	      user=username,
	      passwd=password)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)

	print "Ensure XBMC is at a keyboard entry and start typing..."
	# This code from http://pyfaq.infogami.com/how-do-i-get-a-single-keypress-at-a-time
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
	    while 1:
	        try:
	            c = sys.stdin.read(1)
		    send_key(c)
	        except IOError: pass
	finally:
	    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt, ki:
		pass
