import requests
import json
from bs4 import BeautifulSoup

# No warnings should be displayed on SSL certificates
requests.packages.urllib3.disable_warnings()

########################################################
#Variables needed
########################################################

username='admin'
passwd='techX2019!'
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
def CheckURL(URL,username,passwd):
    # Get the anwser from the URL
    anwser=requests.get(URL,verify=False,auth=(username,passwd),timeout=5)
    try:
        json_data=json.loads(anwser.text)[0]
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

    # Call the URL Get function
    json_data=CheckURL(URL,username,passwd)

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

    # -----------------------------------------------------------------
    # Check to see if the AFS is downloaded and ready to be deployed???
    # -----------------------------------------------------------------
    PrintSeperator('Nutanix Files pre-requirements')

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v1/upgrade/afs/softwares"

    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd)

    # Get the entities and transform into a dictionary for searching
    json_dict=dict(json_data['entities'][5])

    # If all loaded and completed all good...
    if json_dict['version'] == '3.2.0.1' and json_dict['status'] == 'COMPLETED':
        print('Check OK...')
    else:
        print("Issue seen at AFS... Please check.")
        print('Version: ' + json_dict['version'] + " Status = " + json_dict['status'])

    # -----------------------------------------------------------------
    # Check to see if the AFS is downloaded and ready to be deployed???
    # -----------------------------------------------------------------
    PrintSeperator('Images on the clusters..')

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway//services/rest/v2.0/images/"

    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd)

    # How much images do we have?
    images_dict=json_data['metadata']
    images_nr=images_dict['grand_total_entities']

    # minimum amount of images must be 15!!! If not check the name and type
    if images_nr >= 15:
        for image in range(int(images_nr)):
            if '.iso' in dict(json_data['entities'][image])['name']:
                if dict(json_data['entities'][image])['image_type']=='ISO_IMAGE':
                    Image_check=True
                else:
                    Image_check=False
                    print('ERROR FOUND:')
                    print('Name is :' + dict(json_data['entities'][image])['name'] + ', type= ' + dict(json_data['entities'][image])['image_type'])
            elif any(x in dict(json_data['entities'][image])['name'] for x in imagename):
                if dict(json_data['entities'][image])['image_type']=='DISK_IMAGE':
                    Image_check=True
                else:
                    Image_check=False
                    print('ERROR FOUND:')
                    print('Name is :' + dict(json_data['entities'][image])['name'] + ', type= ' + dict(json_data['entities'][image])['image_type'])
        # If the images check out and their type, print all good!        
        if Image_check:
            print('Check OK...')
    else:
        # Not ok. The minimum amount of 15 has not been seen. Print a full list of the images available
        print('ERROR FOUND: To little images (' + str(images_nr) +') found.. The following images have been found....')
        for image in range(int(images_nr)):

            print('Name is :' + dict(json_data['entities'][image])['name'] + ', type= ' + dict(json_data['entities'][image])['image_type'])

    # -----------------------------------------
    # Check to see if the network defined is ok
    # -----------------------------------------
    PrintSeperator('Networking on the clusters..')

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v2.0/networks/"

    # Get the anwser json from the API call
    json_data=CheckURL(URL,username,passwd)


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
    # Check to see if Calm is installed
    # -----------------------------------------
    PrintSeperator('Checking Calm..')

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/apps/projects'

    # Get the response from the site
    bs_data=requests.get(URL,verify=False,auth=(username,passwd))
    bs_content=BeautifulSoup(bs_data.content, 'html.parser')
    try:
        if 'var CALM_VERSION = \'2.4.0\' || \'Unknown\';' in bs_content.script.string:
            print('Check OK...')
    except:
        print('ERROR FOUND:')
        print('Calm has not been found or is not enabled...')



########################################################
# Main Routine
########################################################
for IP in open('clusterIP.txt','r'):
    CheckRoutine(IP.strip())