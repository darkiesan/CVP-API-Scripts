#!/usr/bin/python

import cvp, optparse, json, sys
from string import Template

#
# Prepate command line options
#
usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-c', '--cvphostname', dest='cvphostname', action='store', help='CVP host name FQDN or IP', type='string', default='')
op.add_option( '-u', '--cvpusername', dest='cvpusername', action='store', help='CVP username', type='string', default='')
op.add_option( '-p', '--cvppassword', dest='cvppassword', action='store', help='CVP password', type='string', default='')
op.add_option( '-s', '--switchname', dest='switchname', action='store', help='Substring in switchname to look for', type='string', default='')
op.add_option( '-i', '--imagebundlename', dest='imagebundlename', action='store', help='Image bundle name as named in CVP', type='string', default='')

#
# Parse the command line
#
opts, _ = op.parse_args()

#
# Check so that command options have been provided
#

if opts.cvphostname == "" or opts.cvpusername == "" or opts.cvppassword == "" or opts.switchname == "" or opts.imagebundlename == "":
	print "Please provide all command line options"
	sys.exit(0)

#
# Fetch command like options into variables
#
host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
switchname = opts.switchname
imagebundlename = opts.imagebundlename

#
# Connect to CVP
#
server = cvp.Cvp( host )
server.authenticate( user , password )

#
# Get all devices
#
devices = server.getDevices()

#
# Get the Imagebundle to use
#
imagebundle = server.getImageBundle(imagebundlename)

for device in devices:
	if switchname in device.fqdn:
		print "Device %s is using image bundle %s and will be upgraded to %s" % ( device.fqdn , device.imageBundle , imagebundlename )
		server.mapImageBundleToDevice( device, imagebundle )
