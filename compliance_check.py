#!/usr/bin/python

import cvp, optparse

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-c', '--cvphostname', dest='cvphostname', action='store', help='CVP host name FQDN or IP', type='string')
op.add_option( '-u', '--cvpusername', dest='cvpusername', action='store', help='CVP username', type='string')
op.add_option( '-p', '--cvppassword', dest='cvppassword', action='store', help='CVP password', type='string')
op.add_option( '-d', '--container', dest='container', action='store', help='Name of container to use as root for compliance check', type='string')

opts, _ = op.parse_args()

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
containerName = opts.container

server = cvp.Cvp( host )
server.authenticate( user , password )

container = server.getContainer(containerName)
event = server.containerComplianceCheck(container)
print event
