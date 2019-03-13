#!/bin/bash
for i in `seq 1 113`;
do
        echo Connecting to 10.42.${i}.39
        nuclei -server 10.42.${i}.39 -username admin -password techX2019! image.update VeeamBR_9.5.4.2615.Update4.iso image_type=ISO_IMAGE wait=false
        nuclei -server 10.42.${i}.39 -username admin -password techX2019! image.update Nutanix-VirtIO-1.1.3.iso image_type=ISO_IMAGE wait=false
        nuclei -server 10.42.${i}.39 -username admin -password techX2019! image.update Windows2012R2.iso image_type=ISO_IMAGE wait=false
        nuclei -server 10.42.${i}.39 -username admin -password techX2019! image.update SQLServer2014SP3.iso image_type=ISO_IMAGE wait=false
done