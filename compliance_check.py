#!/usr/bin/python

import cvp, optparse, smtplib
from email.mime.text import MIMEText
from string import Template

# Compliance codes for devices and containers
DEVICE_IN_COMPLIANCE = 0
DEVICE_CONFIG_OUT_OF_SYNC = 1
DEVICE_IMAGE_OUT_OF_SYNC = 2
DEVICE_IMG_CONFIG_OUT_OF_SYNC = 3
DEVICE_IMG_CONFIG_IN_SYNC = 4
DEVICE_NOT_REACHABLE = 5
DEVICE_IMG_UPGRADE_REQD = 6
DEVICE_EXTN_OUT_OF_SYNC = 7
DEVICE_CONFIG_IMG_EXTN_OUT_OF_SYNC = 8
DEVICE_CONFIG_EXTN_OUT_OF_SYNC = 9
DEVICE_IMG_EXTN_OUT_OF_SYNC = 10
DEVICE_UNAUTHORIZED_USER = 11

complianceCodes = {
   DEVICE_IN_COMPLIANCE : 'In compliance',
   DEVICE_CONFIG_OUT_OF_SYNC : 'Config out of sync',
   DEVICE_IMAGE_OUT_OF_SYNC : 'Image out of sync',
   DEVICE_IMG_CONFIG_OUT_OF_SYNC : 'Image and Config out of sync',
   DEVICE_IMG_CONFIG_IN_SYNC : 'Unused',        # was: 'Image and Config in sync'
   DEVICE_NOT_REACHABLE : 'Device not reachable',
   DEVICE_IMG_UPGRADE_REQD : 'Image upgrade required',
   DEVICE_EXTN_OUT_OF_SYNC : 'Extensions out of sync',
   DEVICE_CONFIG_IMG_EXTN_OUT_OF_SYNC : 'Config, Image and Extensions out of sync',
   DEVICE_CONFIG_EXTN_OUT_OF_SYNC : 'Config and Extensions out of sync',
   DEVICE_IMG_EXTN_OUT_OF_SYNC : 'Image and Extensions out of sync',
   DEVICE_UNAUTHORIZED_USER : 'Unauthorized User',
}

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
body = ""

for device in devices:
	compliance = server.deviceComplianceCheck(device)
	if compliance != 0:
		nonCompliantMessage = complianceCodes[compliance]
		nonCompliantDevice = {	'device': device.fqdn,
								'message': nonCompliantMessage }
		nonCompliant.append(nonCompliantDevice)

print nonCompliant

if nonCompliant:
	for i in range(len(nonCompliant)):
		print i
		Replacements = {
							'device': nonCompliant[i]['device'],
							'message': nonCompliant[i]['message']
						}
    	tmpbody = Template("""
Device $device is non-compliant due to: $message

""").safe_substitute(Replacements)
    	body = body + tmpbody
    	print tmpbody

msg = MIMEText(body)
msg['Subject'] = 'Device compliance report'
msg['From'] = email
msg['To'] = recipient
msg = msg.as_string()

#	try:
#		emailserver = smtplib.SMTP(smtpserver, 25)
#		emailserver.sendmail(email, recipient, msg)
#		emailserver.quit()
#	except:
#		raise