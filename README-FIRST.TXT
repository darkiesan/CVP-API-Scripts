=================
fabric-builder.py
=================
This is a script that takes arguments and based on that input data it builds
configlets and container structure in CVP via the CVP API. All needed after that
is to add elements via CVP ZTP or manual addition to CVP and add configlets to
correct devices.

The script was intended for building labs quick, but can be used if templates in
script is altered to suite customer needs to deploy customer networks.

The script can deploy fabric of the type HER (Head End Replication), CVX and EVPN.
Please note that for CVX, a separate configlet is needed today for the actual 
management cvx config for the leafs and a separate configlet for the actual CVX instance.
This scripts merely builds all other config needed for these types of fabrics.

Also a few assumptions are made like ASN can be 65000 for all spines and 65001 for all
leafs in HER/CVX deploments. And for EVPN deployments leafs start with 65001 and up with
an ASN unique for each leaf. EVPN spines all stay with ASN 65000.

I also urge you to study the script to see all needed arguments, since these are critical
to construct correct config. Use the -a yes to see the proposed config in the terminal
before using -a no to actually deploy in your CVP.

=================
mlag-upgrade.py
=================
This script is intended to use the CVP API to assign an existing image bundle in CVP known by name to
each switch identified by the argument that matches switches in the script. I.e.
meant to assign image bundle to one member per MLAG pair in CVP identified by the
argument. When image bundle is assigned, please use CVP GUI to create a changek control
task to be able to upgarde with snapshots and rollback capabilities. When the first upgrade
is finished, the script can be used again to match the other member of each MLAG pair and
then go on again to change control task management.

=======================
vxlan_provision_cvp_api
=======================
This is an example to show how VXLAN provisioning can be done for all switches using
a CVP API script. The script assumes in its current state a CVX setup, but can simply
if needed to be altered to cover HER aswell. The script also wants an interface to assign
the actual VLAN to and whether that is an access port or trunk port. This results in a
configlet assigned to the device sent as an argument to the switch. This means each provisioning
will have one configlet each, so it is easy to add and remove when needed per device.
The script does not however create the VLAN and thus it is not removed either if the provisioning
is removed. These things might change in future versions of the script.

