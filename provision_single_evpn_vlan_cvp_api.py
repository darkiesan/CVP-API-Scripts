#!/usr/bin/env python

import cvp, optparse, json
from jsonrpclib import Server
from string import Template

#
# Parse command line options
#

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-c', '--cvphostname', dest='cvphostname', action='store', help='CVP host name FQDN or IP', type='string')
op.add_option( '-u', '--cvpusername', dest='cvpusername', action='store', help='CVP username', type='string')
op.add_option( '-p', '--cvppassword', dest='cvppassword', action='store', help='CVP password', type='string')
op.add_option( '-d', '--devices', dest='devices', action='store', help='Name of devices to deploy EVPN config on', type='string')
op.add_option( '-v', '--vlan', dest='vlan', action='store', help='VLAN for EVPN', type='string')
op.add_option( '-n', '--vrfname', dest='vrfname', action='store', help='Name of VRF to use in EVPN', type='string')
op.add_option( '-i', '--vlanip', dest='vlanip', action='store', help='IP address for vlan interface', type='string')
op.add_option( '-m', '--netmask', dest='netmask', action='store', help='Netmask for vlan interface', type='string')


opts, _ = op.parse_args()

#
# Assign command line options to variables and assign static variables
#

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
devices = opts.devices
deviceList = devices.split()
vlan = opts.vlan
vxlanid = str(int(vlan) + 10000)
vrfid = str(int(vlan) + 20000)
vrfname = opts.vrfname
vlanip = opts.vlanip
netmask = opts.netmask

#
# Create needed configlets for the new DC
#

for device in deviceList:

	server = cvp.Cvp( host )
	server.authenticate( user , password )

	mydevices = server.getDevices()
	for mydevice in mydevices:
		if mydevice.fqdn == device:
			ip = mydevice.ipAddress

	EAPI_user = user
	EAPI_pass = password
	EAPI_method = 'http'

	switch = Server( '%s://%s:%s@%s/command-api' % ( EAPI_method, EAPI_user, EAPI_pass, ip ) )
	response = switch.runCmds(1, ["enable", "show ip bgp summary"])
	asnumber = response[1]['vrfs']['default']['asn']
	response = switch.runCmds(1, ["enable", "show interfaces Loopback0"])
	routerid = response[1]['interfaces']['Loopback0']['interfaceAddress'][0]['primaryIp']['address']

	Replacements = {
						"vrfname": vrfname,
						"vlan": vlan,
						"vxlanid": vxlanid,
						"vrfid": vrfid,
						"asnumber": asnumber,
						"loopbackip": routerid,
						"ipaddress": vlanip,
						"netmask": netmask
            	    	}

	evpn_config = Template("""
!
vrf definition $vrfname
!
ip routing vrf $vrfname
!
vlan $vlan
!
interface vxlan1
   vxlan vlan $vlan vni $vxlanid
   vxland vrf $vrfname vni $vrfid
!
interface Vlan$vlan
   vrf forwarding $vrfname
   ip address virtual $ipaddress/$netmask
!
router bgp $asnumber
   vlan $vlan
      rd $vxlanid:$loopbackip
      route-target both $asnumber:$vxlanid
      redistribute learned
   vrf $vrfname
      rd $vxlanid:$loopbackip
      route-target both $asnumber:$vrfid
      redistribute connected
""").safe_substitute(Replacements)

	evpn_configlet_name = "Customer " + vrfname + " EVPN instance for VXLAN/VLAN " + vlan
	evpn_configlet = cvp.Configlet( evpn_configlet_name , evpn_config  )
	server.addConfiglet( evpn_configlet )
	configlet_list = []
	configlet_list.append(evpn_configlet)

#
# Find the device in CVP and add configlet to it
#

	for mydevice in mydevices:
		if mydevice.fqdn == device:
			server.mapConfigletToDevice( mydevice , configlet_list )