#!/usr/bin/env python

import cvp, optparse, json
from string import Template

#
# Parse command line options
#

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-c', '--cvphostname', dest='cvphostname', action='store', help='CVP host name FQDN or IP', type='string')
op.add_option( '-u', '--cvpusername', dest='cvpusername', action='store', help='CVP username', type='string')
op.add_option( '-p', '--cvppassword', dest='cvppassword', action='store', help='CVP password', type='string')
op.add_option( '-d', '--device', dest='device', action='store', help='Name of device to deploy interface description on', type='string')
op.add_option( '-x', '--description', dest='description', action='store', help='Interface description', type='string')
op.add_option( '-i', '--interface', dest='interface', action='store', help='Interface to deply description on', type='string')

opts, _ = op.parse_args()

#
# Assign command line options to variables and assign static variables
#

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
device = opts.device
description = opts.description
interface = opts.interface

#
# Connect and authenticate with CVP server
#

server = cvp.Cvp( host )
server.authenticate( user , password )

#
# Create needed configlets for the new DC
#

Replacements = {
					"interface": interface,
					"description": description

                	}

description_config = Template("""
	!
	interface $interface
       description $description
	""").safe_substitute(Replacements)

description_configlet_name = "Interface description for interface " + interface

description_configlet = cvp.Configlet( description_configlet_name , description_config  )
server.addConfiglet( description_configlet )
configlet_list = []
configlet_list.append(description_configlet)

#
# Find the device in CVP and add configlet to it
#

devices = server.getDevices()

for mydevice in devices:
	if mydevice.fqdn == device:
		server.mapConfigletToDevice( mydevice , configlet_list )