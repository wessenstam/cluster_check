#!/bin/bash
#
#
#       This script is for staging the DR Runbooks lab DNS Entries on AutoDC
#
#       Created by Nathan Cox 2/11/19
#
#       Update by | Date
#       JNC           | 2/11/19
#
#
BIN=/usr/bin
DOMAIN=ntnxlab.local
PASSWD="nutanix/4u"
AUTODCLIST=/root/gts2019_autodc_list.csv
DCLIST=`cat /root/gts2019_dc_list.txt`
OLDIFS=$IFS
IFS=,

#for each in $AUTODCLIST
[ ! -f $AUTODCLIST ] && { echo "$AUTODCLIST file not found"; exit 99; }
while read -u30 Input1 Input2 Input3 Input4 Input5 Input6
do
    DC=$Input1
    DRWEB=$Input2
    DRWEBIP=$Input3
    DRDB=$Input4
    DRDBIP=$Input5
    echo ""
    echo "-------"
    echo ""
    echo "AutoDC : $DC"
    echo "DRWeb : $DRWEB"
    echo "DRWeb IP ; $DRWEBIP"
    echo "DRDB : $DRDB"
    echo "DRDB IP : $DRDBIP"
    echo ""
    SSHPASS=$PASSWD sshpass -e ssh root@$DC 'pwd'
    #
    # Add DNS Entries for DRWebX and DRDBX #
    #
    SSHPASS=$PASSWD sshpass -e ssh root@$DC "samba-tool dns delete $DC $DOMAIN $DRWEB A $DRWEBIP -U administrator --password $PASSWD; samba-tool dns delete $DC $DOMAIN $DRDB A $DRDBIP -U administrator --password $PASSWD"
    echo ""
    echo "-------"
    echo ""
done 30< $AUTODCLIST
IFS=$OLDIFS
for DC in $DCLIST
do
    echo ""
    echo "-------"
    echo ""
    echo ""
    echo $DC
    echo ""
    echo ""
    SSHPASS=$PASSWD sshpass -e ssh root@$DC "samba-tool dns query $DC $DOMAIN @ ALL -U administrator --password $PASSWD"
    echo ""
    echo ""
    echo "-------"
    echo ""
done