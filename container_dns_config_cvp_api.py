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
op.add_option( '-d', '--container', dest='container', action='store', help='Name of container to deploy DNS config to', type='string')
op.add_option( '-x', '--dnsconfig', dest='dnsconfig', action='store', help='IP of DNS', type='string')
op.add_option( '-i', '--domainname', dest='domainname', action='store', help='Domainname', type='string')

opts, _ = op.parse_args()

#
# Assign command line options to variables and assign static variables
#

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
container = opts.container
dnsconfig = opts.dnsconfig
domainname = opts.domainname

#
# Connect and authenticate with CVP server
#

server = cvp.Cvp( host )
server.authenticate( user , password )

#
# Create needed configlets for the new DC
#

Replacements = {
					"dnsconfig": dnsconfig,
					"domainname": domainname

                	}

dns_config = Template("""
	!
	ip name-server $dnsconfig
	ip domain-name $domainname
""").safe_substitute(Replacements)

dns_configlet_name = "DNS config for container " + container

dns_configlet = cvp.Configlet( dns_configlet_name , dns_config  )
server.addConfiglet( dns_configlet )
configlet_list = []
configlet_list.append(dns_configlet)

#
# Find the device in CVP and add configlet to it
#

containers = server.getContainers()

for mycontainer in containers:
	if mycontainer.name == container:
		server.mapConfigletToContainer( mycontainer , configlet_list )