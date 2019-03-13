#!/usr/bin/python

import sys
sys.path.insert(0, '/home/nutanix/ncc/bin')
import env
import os
import requests

# resolve all alerts
requests.packages.urllib3.disable_warnings()
url = "https://localhost:9440/PrismGateway/services/rest/v2.0/alerts/resolve"
ret = requests.post(url, auth=("admin", "techX2019!"), verify=False)
print ret

# execute policy check
os.system("python ~/ncc/bin/health_client.py --run_sync=True health_checks policy_checks all_policy_checks")
