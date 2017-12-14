#!/usr/bin/python

import cvp, optparse, smtplib
from email.mime.text import MIMEText
from string import Template

usage = 'usage: %prog [options]'
op = optparse.OptionParser(usage=usage)
op.add_option( '-c', '--cvphostname', dest='cvphostname', action='store', help='CVP host name FQDN or IP', type='string')
op.add_option( '-u', '--cvpusername', dest='cvpusername', action='store', help='CVP username', type='string')
op.add_option( '-p', '--cvppassword', dest='cvppassword', action='store', help='CVP password', type='string')
op.add_option( '-e', '--email', dest='email', action='store', help='Sender address for email', type='string')
op.add_option( '-r', '--recipient', dest='recipient', action='store', help='Recipient address for email', type='string')
op.add_option( '-s', '--smtpserver', dest='smtpserver', action='store', help='IP address for SMTP server', type='string')

opts, _ = op.parse_args()

host = opts.cvphostname
user = opts.cvpusername
password = opts.cvppassword
email = opts.email
recipient = opts.recipient
smtpserver = opts.smtpserver

server = cvp.Cvp( host )
server.authenticate( user , password )

#container = server.getContainer(containerName)
#events = server.containerComplianceCheck(container)

#for event in events:
#	print event.complianceCode

devices = server.getDevices()
nonCompliant = []

for device in devices:
	compliance = server.deviceComplianceCheck(device)
	if compliance != 0:
		nonCompliantMessage = complianceCodes[compliance]
		nonCompliantDevices = { 'device': device.fqdn,
								'message': nonCompliantMessage }
		nonCompliant.append(nonCompliantDevice)

if nonCompliant:
	for nonCompliantDevice in nonCompliant:
		Replacements = {
							'device': nonCompliantDevice['device'],
							'message': nonCompliantDevice['message']
						}
    	tmpbody = Template("""
Device $device is non-compliant due to: $message

""").safe_substitute(Replacements)
    	body = body + tmpbody

	msg = MIMEText(body)
	msg['Subject'] = 'Device compliance report'
	msg['From'] = email
	msg['To'] = recipient
	msg = msg.as_string()
    	try:
        	emailserver = smtplib.SMTP(smtpserver, 25)
	    except:
    	    raise