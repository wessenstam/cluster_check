_amount_entries=$(curl -X POST \
  https://10.42.23.39:9440/api/nutanix/v3/groups \
  -H 'Authorization: Basic YWRtaW46dGVjaFgyMDE5IQ==' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 825205c1-e60e-453e-ac05-124be59791c2' \
  -H 'cache-control: no-cache' \
  --insecure --silent \
  -d '{"entity_type":"lcm_entity","grouping_attribute":"entity_class","group_member_count":1000,"group_member_attributes":[{"attribute":"id"},{"attribute":"uuid"},{"attribute":"entity_model"},{"attribute":"version"},{"attribute":"location_id"},{"attribute":"entity_class"},{"attribute":"description"},{"attribute":"last_updated_time_usecs"},{"attribute":"request_version"},{"attribute":"_master_cluster_uuid_"}],"query_name":"prism:LCMQueryModel","filter_criteria":"_master_cluster_uuid_==[no_val]"}' | jq '.total_entity_count')

 echo $_amount_entries 