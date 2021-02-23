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

    ########################################################
    PrintSeperator(clusterIP)
    ########################################################

    # -------------------------------------------------
    # PC Registered and reachable???
    # -------------------------------------------------
    PrintSeperator('PRISM Central connectivity')

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

    if json_dict['reachable']:
        print("Check OK...")
    else:
        print('ERROR FOUND! There is an issue with cluster ' + clusterIP + ' and PC')


    # -----------------------------------------
    # Check to see if the network defined is ok
    # -----------------------------------------
    PrintSeperator('Networking on the clusters..')

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v2.0/networks/"
    payload = ""
    method = "GET"
    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd,payload,method)


    # Check all the networks that have been defined.
    # Get the number of networks
    for nr in range(int(dict(json_data['metadata'])['total_entities'])) :
        # print name of the network
        if json_data['entities'][nr]['name'] == 'Primary':
            if any(x in dict(json_data['entities'][nr]['ip_config'])['pool'][0]['range'] for x in PrimNet):
                NetworkCheck=True
            else:
                NetworkCheck=False
                print('ERROR FOUND:')
                print('Name is :' + json_data['entities'][nr]['name'] + ', IP Range= ' + dict(json_data['entities'][nr]['name']))
        elif json_data['entities'][nr]['name'] == 'Secondary':
            if any(x in dict(json_data['entities'][nr]['ip_config'])['pool'][0]['range'] for x in SecNet):
                NetworkCheck=True
            else:
                NetworkCheck=False
                print('ERROR FOUND:')
                print('Name is :' + json_data['entities'][nr]['name'] + ', IP Range= ' + dict(json_data['entities'][nr]['ip_config'])['pool'][0]['range'])
        else:
            print('ERROR FOUND:')
            try:
                print('Name is :' + json_data['entities'][nr]['name'] + ', IP Range= ' + dict(json_data['entities'][nr]['ip_config'])['pool'][0]['range'])
            except:
                print('Name is :' + json_data['entities'][nr]['name'])

    if NetworkCheck:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if Calm has 4 BPS
    # -----------------------------------------
    PrintSeperator('Checking Calm BPs..')

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/blueprints/list'
    payload = "{}"
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 4:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if Calm has 16 Apps
    # -----------------------------------------
    PrintSeperator('Checking Calm Apps..')

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/apps/list'
    payload = "{}"
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 16:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if there is a objects store
    # -----------------------------------------
    PrintSeperator('Checking Objects store..')

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/oss/api/nutanix/v3/groups'
    payload = '{"entity_type":"objectstore"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['filtered_entity_count']) < 1:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if there are 54 VMs
    # -----------------------------------------
    PrintSeperator('Checking Amount of VMS..')

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/vms/list'
    payload = '{"kind":"vm"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 54:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if Era has 5 Compute profiles
    # -----------------------------------------
    PrintSeperator('Checking Era on 5 Compute profiles..')

    # Era IP is 7 higher than the last octet of the ClusterIP
    ERA_IP=clusterIP[:-2]+str(int(clusterIP[-2:])+7)

    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/profiles?&type=Compute'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 5:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if Era has 5 Network profiles
    # -----------------------------------------
    PrintSeperator('Checking Era on 5 network profiles..')

    # Era IP is 7 higher than the last octet of the ClusterIP
    ERA_IP=clusterIP[:-2]+str(int(clusterIP[-2:])+7)

    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/profiles?&type=Network'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 5:
        print('Check NOK...')
    else:
        print('Check OK...')


    # -----------------------------------------
    # Check to see if Era has 7 DB Servers
    # -----------------------------------------
    PrintSeperator('Checking Era on 7 registered DB servers..')

    # Era IP is 7 higher than the last octet of the ClusterIP
    ERA_IP=clusterIP[:-2]+str(int(clusterIP[-2:])+7)

    # URL to be used
    URL='https://'+ERA_IP+'/era/v0.9/dbservers'
    payload=""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int((len(json_data))) < 7:
        print('Check NOK...')
    else:
        print('Check OK...')

    # -----------------------------------------
    # Check to see if Era has 7 DBs
    # -----------------------------------------
    PrintSeperator('Checking Era on 7 registered DBs..')

    # Era IP is 7 higher than the last octet of the ClusterIP
    ERA_IP = clusterIP[:-2] + str(int(clusterIP[-2:]) + 7)

    # URL to be used
    URL = 'https://' + ERA_IP + '/era/v0.9/databases'
    payload = ""
    method = "GET"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd, payload, method)
    if int((len(json_data))) < 7:
        print('Check NOK...')
    else:
        print('Check OK...')


########################################################
# Main Routine
########################################################
for IP in open('clusterIP.txt','r'):
    CheckRoutine(IP.strip())