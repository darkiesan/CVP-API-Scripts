#!/usr/bin/env python

import cvp
from string import Template

#
# Info needed
#
ip = '192.168.0.5'
user = 'arista'
password = 'arista'
snmp_community = 'kalleolle'
ContainerName = 'Leaf'

cvpServer = cvp.Cvp( ip )
cvpServer.authenticate( user , password )

Replacements = {
					"snmp_community": snmp_community
				}

myConfig = Template("""
snmp-server community $snmp_community ro
""").safe_substitute(Replacements)

myConfigletName = 'Patriks SNMP community'
myConfiglet = cvp.Configlet( myConfigletName, myConfig )

cvpServer.addConfiglet( myConfiglet )

ConfigletList = []
ConfigletList.append(myConfiglet)

myContainer = cvpServer.getContainer( ContainerName )
cvpServer.mapConfigletToContainer( myContainer, ConfigletList )

