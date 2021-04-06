# script to get the VMs of the PCs
# Uses a txt file that has IPADDRESS|PASSWORD|EMAIL|IP ADDRESS PC|SNOW INSTANCE
#!/bin/bash
today=`date '+%Y_%m_%d__%H_%M_%S'`
mkdir -p /root/cluster_staging_files/$today

echo "Dump of all VMS build during the GTS AMER" > /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt
for vars in `cat /root/cluster_staging_files/GTS2021_AMER_Cluster1_Batch*.txt`
do
	var=(${vars//|/ })
	echo "**********************************************" >> /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt

	echo "Dumping the VMs on "${var[3]} >> /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt
	# Fill the array with the DNS servers that are there
	curl -k --silent --user 'USER:PASSWORD' https://${var[3]}:9440/PrismGateway/services/rest/v1/vms | jq '.entities[].vmName' | tr -d \" >> /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt

	# Get the docker vm ip per user and see if Drone is running
	for nr in 1 2 3 4 5 6 7
	do
		IP_docker_vm=$(curl -k --silent --user 'USER:PASSWORD' -H 'Content-Type: application/json' -X POST -d '{"kind": "vm","filter": "vm_name==User0'$nr'-docker_VM"}' "https://${var[3]}:9440/api/nutanix/v3/vms/list" | jq '.entities[0].spec.resources.nic_list[0].ip_endpoint_list[0].ip' | tr -d \")
		Drone_there=$(curl --silent http://$IP_docker_vm:8080 | grep "Drone" | wc -l)
		if [ $Drone_there -gt 0 ]
		then
			echo "Drone is found for User0$nr ..." >> /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt
		fi
	done

	echo "**********************************************" >> /root/cluster_staging_files/$today/VM_Dump_GTS_AMER.txt
done