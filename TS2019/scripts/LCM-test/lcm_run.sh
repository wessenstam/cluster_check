#!/bin/bash
CURL_HTTP_OPTS=' --max-time 25 --silent --header Content-Type:application/json --header Accept:application/json  --insecure --write-out %{http_code}' # --output /dev/null --silent --show-error
PRISM_ADMIN='admin'
PE_PASSWORD='techX2019!'
_url_lcm='https://10.42.8.39:9440/PrismGateway/services/rest/v1/genesis'
_url_progress='https://10.42.8.39:9440/PrismGateway/services/rest/v1/progress_monitors'

###############################################################################################################################################################################
# Routine to be run/loop till yes we are ok.
###############################################################################################################################################################################
function loop(){

  local _attempts=40
  local _error=22
  local _loops=0
  local _sleep=30

  # What is the progress of the taskid?? 
  while true; do
    (( _loop++ ))
    # Get the progress of the task  
    _progress=$(curl ${CURL_HTTP_OPTS} --user ${PRISM_ADMIN}:${PE_PASSWORD} ${_url_progress}?filterCriteria=parent_task_uuid%3D%3D${_task_id} | jq '.entities[0].percentageCompleted' 2>nul | tr -d \")
    if (( ${_progress} == 100 )); then
      echo "The step has been succesfuly run"
      set _error=0
      break;
    elif (( ${_loop} > ${_attempts} )); then
      echo "Warning ${_error} @${1}: Giving up after ${_loop} tries."
      return ${_error}
    else
      echo "Still running... loop $_loop/$_attempts. Step is at ${_progress}% ...Sleeping ${_sleep} seconds"
      sleep ${_sleep}
    fi
  done
}



# Inventory download/run
_task_id=$(curl ${CURL_HTTP_OPTS} --user ${PRISM_ADMIN}:${PE_PASSWORD} -X POST -d '{"value":"{\".oid\":\"LifeCycleManager\",\".method\":\"lcm_framework_rpc\",\".kwargs\":{\"method_class\":\"LcmFramework\",\"method\":\"perform_inventory\",\"args\":[\"http://download.nutanix.com/lcm/2.0\"]}}"}' ${_url_lcm} | jq '.value' 2>nul | cut -d "\\" -f 4 | tr -d \")

# If there has been a reply (task_id) then the URL has accepted by PC
if [ -z "$_task_id" ]; then
  echo "LCM Inventory start has encountered an eror..."
else 
  echo "LCM Inventory started.."
  set _loops=0 # Reset the loop counter

 # Run the progess checker
 loop

 # Set the parameter to create the ugrdae plan
 _task_id=$(curl ${CURL_HTTP_OPTS} --user ${PRISM_ADMIN}:${PE_PASSWORD} -X POST -d '{"value":"{\".oid\":\"LifeCycleManager\",\".method\":\"lcm_framework_rpc\",\".kwargs\":{\"method_class\":\"LcmFramework\",\"method\":\"generate_plan\",\"args\":[\"http://download.nutanix.com/lcm/2.0\",[[\"639b6f37-06c8-4fe0-aeca-5b2c89e61fe6\",\"2.6.0.2\"],[\"dd69fc72-df7f-4195-bb28-6f74eafe353a\",\"2.6.0.2\"]]]}}"}' ${_url_lcm} | jq '.value' 2>nul | cut -d "\\" -f 4 | tr -d \")

 # Notify the log server that the LCM has been creating a plan
 echo "LCM Inventory has created a plan"

 # Run the upgrade to have the latest versions
 _task_id=$(curl ${CURL_HTTP_OPTS} --user ${PRISM_ADMIN}:${PE_PASSWORD} -X POST -d '{"value":"{\".oid\":\"LifeCycleManager\",\".method\":\"lcm_framework_rpc\",\".kwargs\":{\"method_class\":\"LcmFramework\",\"method\":\"perform_update\",\"args\":[\"http://download.nutanix.com/lcm/2.0\",[[\"639b6f37-06c8-4fe0-aeca-5b2c89e61fe6\",\"2.6.0.2\"],[\"dd69fc72-df7f-4195-bb28-6f74eafe353a\",\"2.6.0.2\"]]]}}"}' ${_url_lcm} | jq '.value' 2>nul | cut -d "\\" -f 4 | tr -d \")

# If there has been a reply (task_id) then the URL has accepted by PC
 if [ -z "$_task_id}" ]; then
   # There has been an error!!!
   echo "LCM Upgrade has encountered an error!!!!"
 else
   # Notify the logserver that we are starting the LCM Upgrade
   echo "LCM Upgrade starting..."

  # Run the progess checker
   loop
 fi
fi