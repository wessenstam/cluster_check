import requests
import json
from bs4 import BeautifulSoup

# No warnings should be displayed on SSL certificates
requests.packages.urllib3.disable_warnings()

########################################################
#Variables needed
########################################################

username='admin'
passwd='ntnxGTS2021!'
NetworkCheck=False
Image_check=False
PrimNet=['50','125']
SecNet=['132','229']
imagename=['.qcow2','AutoDC2','CentOS_7_Cloud','.vmdk','acs-centos']

########################################################
# Functions Part
########################################################
# Print some seperation lines
def PrintSeperator(module):
    
    if "10." in module:
        print("*"*40)
        print('Checking the cluster ' + module + '...')
        print("*"*40)
    else:
        print("-"*40)
        print("Checking " + module)
        print("-"*40)
    return

# Function for checking URLs
def CheckURL(URL,username,passwd,payload,method):
    if method=="GET":
        # Get the anwser from the URL
        headers = {"Content-Type": "application/json"}
        anwser=requests.get(URL,verify=False,auth=(username,passwd),timeout=15,headers=headers)
    else:
        headers={"Content-Type": "application/json"}
        anwser = requests.post(URL, verify=False, auth=(username, passwd), timeout=5,data=payload,headers=headers)

    try:
        if "era/v0.9" in URL:
            json_data=json.loads(anwser.text)
        else:
            json_data = json.loads(anwser.text)[0]
        return json_data
    except KeyError:
        json_data=json.loads(anwser.text)
        return json_data
    except:
        return_val='["Error"]'
        return return_val

# Main routine to be run
def CheckRoutine(clusterIP):

    # Get the ERA IP
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v1/multicluster/cluster_external_state"
    payload=""
    method="GET"
    json_data=CheckURL(URL,username,passwd,payload,method)
    ERA_IP=json_data['clusterDetails']['ipAddresses'][0][:-2]+"43"
    

    ########################################################
    PrintSeperator(clusterIP)
    ########################################################

    # -------------------------------------------------
    # PC Registered and reachable???
    # -------------------------------------------------
    

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v1/multicluster/cluster_external_state"
    payload=""
    method="GET"
    # Call the URL Get function
    json_data=CheckURL(URL,username,passwd,payload,method) 

    # If data is not a JSON file, we continue the line
    if 'Error' in json_data:
        print('Have an issue connecting to the Cluster at ' + clusterIP)
        return
    
    # Get the result into a dict so we can search for the right key and value
    json_dict=dict(json_data['clusterDetails'])

    if not json_dict['reachable']:
        PrintSeperator('PRISM Central connectivity')
        print('ERROR FOUND! There is an issue with cluster ' + clusterIP + ' and its PC')


    # -----------------------------------------
    # Check to see if the Name fo the cluster is ok
    # -----------------------------------------
    

    # Url to be checked
    URL="https://"+clusterIP+":9440/api/nutanix/v3/clusters/list"
    payload = "{}"
    method = "POST"
    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd,payload,method)
    if len(json_data['entities'][0]['status']['name']) > 15:
        PrintSeperator('AWS cluster naming')
        print('AWS Cluster ' + clusterIP + ' hasnot been renamed')


    # -----------------------------------------
    # Check to see if the network defined is ok
    # -----------------------------------------
    

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v2.0/networks/"
    payload = ""
    method = "GET"
    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd,payload,method)


    # Check all the networks that have been defined.
    if int(dict(json_data['metadata'])['total_entities']) < 1:
        PrintSeperator('Networking on the clusters..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if there are 2 VMs
    # -----------------------------------------
    
    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/vms/list'
    payload = '{"kind":"vm"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 2:
        PrintSeperator('Checking Amount of VMS..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Era has 2 IDs that way we know AWS has registered to ERA instance
    # -----------------------------------------

    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/clusters'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if len(json_data) < 2:
        PrintSeperator('Checking Era on 2 IDs (did AWS Register)..')
        print('Check NOK...')

"""
    # -----------------------------------------
    # Check to see if Era has 4 Compute profiles
    # -----------------------------------------

    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/profiles?&type=Compute'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 4:
        PrintSeperator('Checking Era on 4 Compute profiles..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Era has 2 Network profiles
    # -----------------------------------------
    
    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/profiles?&type=Network'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 2:
        PrintSeperator('Checking Era on 2 network profile..')
        print('Check NOK...')


    # -----------------------------------------
    # Check to see if Era has 12 Software profiles
    # -----------------------------------------
    
    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/profiles?&type=Software'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 12:
        PrintSeperator('Checking Era on 12 software profile..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Era has 7 DB Servers
    # -----------------------------------------
    
    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/dbservers'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 7:
        PrintSeperator('Checking Era on 7 registered DB servers..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Era has 7 DBs
    # -----------------------------------------

    # URL to be used
    URL = 'https://' + ERA_IP + '/era/v0.9/databases'
    payload = ""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd, payload, method)
    if int((len(json_data))) < 7:
        PrintSeperator('Checking Era on 7 registered DBs..')
        print('Check NOK...')"""


########################################################
# Main Routine
########################################################
for IP in open('cluster2IP.txt','r'):
    CheckRoutine(IP.strip())