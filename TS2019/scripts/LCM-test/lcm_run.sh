#!/bin/bash
CURL_HTTP_OPTS='-X POST --user admin:techX2019! --max-time 25 --header Content-Type:application/json --header Accept:application/json  --insecure --write-out %{http_code}' # --output /dev/null --silent --show-error
_url='https://10.42.100.39:9440/api/nutanix/v3/groups'
_attempts=40
_loops=0
_sleep=10

###############################################################################################################################################################################
# Routine to be run/loop till yes we are ok.
###############################################################################################################################################################################
function loop(){

  while true ; do
      (( _loop++ ))
      _test=$(curl ${CURL_HTTP_OPTS} ${_url} | tr -d \")
      if (( ${_test} == 200 )); then
        echo "Success reaching ${_url}"
        break;
     elif (( ${_loop} > ${_attempts} )); then
        echo "Warning ${_error} @${1}: Giving up after ${_loop} tries."
       return ${_error}
     else
       echo "@${1} ${_loop}/${_attempts}=${_test}: sleep ${_sleep} seconds..."
       sleep ${_sleep}
     fi
    done
}

# Construct the data payload
_data_json="-d '{\"value\":\"{\\\".oid\\\":\\\"LifeCycleManager\\\",\\\".method\\\":\\\"lcm_framework_rpc\\\",\\\".kwargs\\\":{\\\"method_class\\\":\\\"LcmFramework\\\",\\\"method\\\":\\\"perform_inventory\\\",\\\"args\\\":[\\\"http://download.nutanix.com/lcm/2.0\\\"]}}\"}'"

# construct the curl command to be send
CURL_HTTP_OPTS="${CURL_HTTP_OPTS} $_data_json"

curl ${CURL_HTTP_OPTS} ${_url}
#_test=$(curl ${CURL_HTTP_OPTS} ${_url} \
#  -d '{"value":"{\".oid\":\"LifeCycleManager\",\".method\":\"lcm_framework_rpc\",\".kwargs\":{\"method_class\":\"LcmFramework\",\"method\":\"perform_inventory\",\"args\":[\"http://download.nutanix.com/lcm/2.0\"]}}"}' https://10.42.5.39:9440/PrismGateway/services/rest/v1/genesis | tr -d \")

#  if (( ${_test} == 200 )); then
#    echo "YES!!!"
#  else
#    echo "NO!!!"
#  fi
