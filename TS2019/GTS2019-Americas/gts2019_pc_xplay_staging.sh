#!/bin/bash
#
#
#       This script is for staging the Xplay lab on Prism Central ver 5.10.x
#
#       Created by Nathan Cox 2/11/19
#
#       Update by | Date
#       JNC           | 2/11/19
#
#

DATE=`date +%H%M%S-%m%d%Y`
PASSWD="nutanix/4u"

#PRISMCENTRALLIST=`cat /Users/nathancox/Development/gts2019_prismcentral_list.csv`
PRISMCENTRALLIST=`cat /root/gts2019_prismcentral_list.txt`

UNLOCKXPLAYURL="https://s3.amazonaws.com/get-ahv-images/unlockxplay.py"
PAINTRIGGERURL="https://s3.amazonaws.com/get-ahv-images/paintrigger.py"

for PC in $PRISMCENTRALLIST
do
    echo ""
    echo "-------"
    echo ""
    echo ""
    echo $PC
    SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'pwd'
    #
    # Download the two Python Scripts #
    #
    #SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'curl -L https://s3.amazonaws.com/get-ahv-images/unlockxplay.py -o /home/nutanix/unlockxplay.py'
    #SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'curl -L https://s3.amazonaws.com/get-ahv-images/paintrigger.py -o /home/nutanix/paintrigger.py'
    #
    SSHPASS=$PASSWD sshpass -e scp /root/unlockxplay.py nutanix@$PC:/home/nutanix/.
    SSHPASS=$PASSWD sshpass -e scp /root/paintrigger.py nutanix@$PC:/home/nutanix/.
    #
    #
    SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'chmod +x /home/nutanix/unlockxplay.py'
    SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'chmod +x  /home/nutanix/paintrigger.py'
    #
    # Execute the Python Script to unlock Xplay functionality in PC 5.10.x #
    #
    SSHPASS=$PASSWD sshpass -e ssh nutanix@$PC 'python /home/nutanix/unlockxplay.py'
    #
    echo ""
        echo "-------"
        echo ""
done