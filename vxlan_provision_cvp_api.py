#!/usr/bin/python

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
op.add_option( '-d', '--device', dest='device', action='store', help='Name of device to deploy VXLAN/VLAN on', type='string')
op.add_option( '-v', '--vlan', dest='vlan', action='store', help='VLAN to deploy', type='int')
op.add_option( '-i', '--interface', dest='interface', action='store', help='Interface to deply vlan on', type='string')
op.add_option( '-t', '--trunk', dest='trunk', action='store', help='Is interface a trunk or access port for VLAN', type='string')



opts, _ = op.parse_args()

#
# Assign command line options to variables and assign static variables
#

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
device = opts.device
vlan = opts.vlan
interface = opts.interface
trunk = opts.trunk

#
# Build needed variables
#

vni = vlan + 10000
vxlan_configlet_name = "VXLAN " + str(vni) + " and VLAN " + str(vlan) + " on device " + str(device)

#
# Connect and authenticate with CVP server
#

server = cvp.Cvp( host )
server.authenticate( user , password )

#
# Create needed configlets for the new DC
#

if trunk == "yes":
	Replacements = {
    	            "vlan": vlan,
        	        "vni": vni,
            	    "interface": interface,
                	}

	vxlan_config = Template("""
	!
	interface vxlan1
	   vxlan vlan $vlan vni $vni
	!
	interface $interface
	   switchport mode trunk
	   switchport trunk allowed vlan add $vlan
	""").safe_substitute(Replacements)

if trunk == "no":
	Replacements = {
    	            "vlan": vlan,
        	        "vni": vni,
            	    "interface": interface,
                	}

	vxlan_config = Template("""
	!
	interface vxlan1
	   vxlan vlan $vlan vni $vni
	!
	interface $interface
	   switchport access vlan $vlan
	""").safe_substitute(Replacements)

vxlan_configlet = cvp.Configlet( vxlan_configlet_name , vxlan_config  )
server.addConfiglet( vxlan_configlet )
configlet_list = []
configlet_list.append(vxlan_configlet)

#
# Find the device in CVP and add configlet to it
#

devices = server.getDevices()

for mydevice in devices:
	if mydevice.fqdn == device:
		server.mapConfigletToDevice( mydevice , configlet_list )