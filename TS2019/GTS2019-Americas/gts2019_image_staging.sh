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

curl -L https://s3.amazonaws.com/get-ahv-images/AutoDC2.qcow2 -o /usr/share/nginx/html/images/AutoDC2.qcow2 

#OS Images:
#curl -L  https://s3.amazonaws.com/get-ahv-images/CentOS7.iso -o /usr/share/nginx/html/images/CentOS7.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/CentOS7.qcow2 -o /usr/share/nginx/html/images/CentOS7.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows10.iso -o /usr/share/nginx/html/images/Windows10.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows10-1709.qcow2 -o /usr/share/nginx/html/images/Windows10-1709.qcow2 
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows2012R2.iso -o /usr/share/nginx/html/images/Windows2012R2.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows2012R2.qcow2 -o /usr/share/nginx/html/images/Windows2012R2.qcow2 
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows2016.iso -o /usr/share/nginx/html/images/Windows2016.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/Windows2016.qcow2 -o /usr/share/nginx/html/images/Windows2016.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/Nutanix-VirtIO-1.1.3.iso -o /usr/share/nginx/html/images/Nutanix-VirtIO-1.1.3.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/ToolsVM.qcow2 -o /usr/share/nginx/html/images/ToolsVM.qcow2

#Karbon OS Images:
#curl -L  https://s3.amazonaws.com/get-ahv-images/acs-centos7.qcow2 -o /usr/share/nginx/html/images/acs-centos7.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/acs-ubuntu1604.qcow2 -o /usr/share/nginx/html/images/acs-ubuntu1604.qcow2

#Nutanix Software:
#curl -L  https://s3.amazonaws.com/get-ahv-images/pcdeploy-5.10.1.1.json -o /usr/share/nginx/html/images/pcdeploy-5.10.1.1.json
#curl -L  https://s3.amazonaws.com/get-ahv-images/euphrates-5.10.1.1-stable-prism_central.tar -o /usr/share/nginx/html/images/euphrates-5.10.1.1-stable-prism_central.tar
#curl -L  https://s3.amazonaws.com/get-ahv-images/xtract-vm-2.0.3.qcow2 -o /usr/share/nginx/html/images/xtract-vm-2.0.3.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/ERA-Server-build-1.0.1.qcow2 -o /usr/share/nginx/html/images/ERA-Server-build-1.0.1.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/sherlock-k8s-base-image_320.qcow2 -o /usr/share/nginx/html/images/sherlock-k8s-base-image_320.qcow2
curl -L  https://s3.amazonaws.com/get-ahv-images/sherlock-k8s-base-image_403.qcow2 -o /usr/share/nginx/html/images/sherlock-k8s-base-image_403.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/nutanix-afs-el7.3-release-afs-3.2.0.1-stable.qcow2 -o /usr/share/nginx/html/images/nutanix-afs-el7.3-release-afs-3.2.0.1-stable.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/nutanix-afs-el7.3-release-afs-3.2.0.1-stable-metadata.json -o /usr/share/nginx/html/images/nutanix-afs-el7.3-release-afs-3.2.0.1-stable-metadata.json

#EUC Infra:
#curl -L  https://s3.amazonaws.com/get-ahv-images/XenApp_and_XenDesktop_7_18.iso -o /usr/share/nginx/html/images/XenApp_and_XenDesktop_7_18.iso
#curl -L  https://s3.amazonaws.com/get-ahv-images/SQLServer2014SP3.iso -o /usr/share/nginx/html/images/SQLServer2014SP3.iso

#Partner Software:
#curl -L  https://s3.amazonaws.com/get-ahv-images/hycu-3.5.0-6253.qcow2 -o /usr/share/nginx/html/images/hycu-3.5.0-6253.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/hycu-3.5.0-6138.qcow2 -o /usr/share/nginx/html/images/hycu-3.5.0-6138.qcow2
#curl -L  https://s3.amazonaws.com/get-ahv-images/VeeamAvailability_1.0.457.vmdk -o /usr/share/nginx/html/images/VeeamAvailability_1.0.457.vmdk
#curl -L  https://s3.amazonaws.com/get-ahv-images/VeeamBR_9.5.4.2615.Update4.iso -o /usr/share/nginx/html/images/VeeamBR_9.5.4.2615.Update4.iso