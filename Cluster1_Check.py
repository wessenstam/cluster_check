import requests
import json
import time

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
SecNet=['132','208']
imagename=['.qcow2','AutoDC2','CentOS_7_Cloud','.vmdk','acs-centos']

karbon_nok={}

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
        anwser = requests.post(URL, verify=False, auth=(username, passwd), timeout=15,data=payload,headers=headers)

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

def openkarbon_ui(ip,user,passwd):
    options=Options()
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    try:
        driver = webdriver.Chrome("./chromedriver",options=options)
        driver.get("https://"+ip+":9440/console/#page/karbon")
        delay = 10
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'inputUsername')))
            time.sleep(5)
            driver.find_element_by_id("inputUsername").send_keys(Keys.NULL)
            driver.find_element_by_id("inputUsername").send_keys(user)
            driver.find_element_by_id("inputUsername").send_keys(Keys.TAB)
            time.sleep(1)
            driver.find_element_by_id("inputPassword").send_keys(passwd)
            driver.find_element_by_id("inputPassword").send_keys(Keys.ENTER)
            time.sleep(20)
            driver.quit()
        except TimeoutException:
            print("Loading took too much time!")
            driver.quit()
    except:
            print("Cluster "+ip+" is not accesible...")
            return "Fail"

# Main routine to be run
def CheckRoutine(clusterIP):

    ########################################################
    PrintSeperator(clusterIP)
    ########################################################

    # -------------------------------------------------
    # All 4 nodes there ???
    # -------------------------------------------------
    

    # Url to be checked
    URL="https://"+clusterIP+":9440/PrismGateway/services/rest/v1/clusters"
    payload=""
    method="GET"
    # Call the URL Get function
    json_data=CheckURL(URL,username,passwd,payload,method)
    try:
        if int(json_data['entities'][0]['numNodes']) < 4:
            PrintSeperator('Cluster nodes.')
            print('ERROR FOUND! There are not 4 nodes in cluster with IP Address: ' + clusterIP)
    except:
        print("Couldn't get a connection to cluster "+clusterIP+". Please check the cluster...")
        return

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
        print('Have an issue connecting to get the IP of the PC for Cluster at ' + clusterIP)
        return
    
    # Get the result into a dict so we can search for the right key and value
    json_dict=dict(json_data['clusterDetails'])

    if not json_dict['reachable']:
        PrintSeperator('PRISM Central connectivity')
        print('ERROR FOUND! There is an issue with cluster ' + clusterIP + ' and PC')


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
    if int(dict(json_data['metadata'])['total_entities']) < 2:
        PrintSeperator('Networking on the clusters..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Calm has 3 BPS
    # -----------------------------------------
    

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/blueprints/list'
    payload = "{}"
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 3:
        PrintSeperator('Checking Calm BPs..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if Calm has 9 Apps running
    # -----------------------------------------
  

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/apps/list'
    payload = "{}"
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    value=0
    error_value=0
    app_name=[]
    # Try to get the ones that did not start
    for nr in range(int(json_data['metadata']['total_matches'])):
        if json_data['entities'][nr]['status']['state'] == "running":
            value += 1
        else:
            app_name.append(json_data['entities'][nr]['status']['name'])
            error_value += 1

    if value < 9:
        PrintSeperator('Checking Calm Apps..')
        for i in range(error_value):
            print ("App :"+app_name[i]+" is not in running state...")
        print("Check: NOK...")


    # -----------------------------------------
    # Check to see if there is a objects store
    # -----------------------------------------
    

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/oss/api/nutanix/v3/groups'
    payload = '{"entity_type":"objectstore"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['filtered_entity_count']) < 1:
        PrintSeperator('Checking Objects store..')
        print('Check NOK...')

    # -----------------------------------------
    # Check to see if there are 28 VMs
    # -----------------------------------------
    

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/api/nutanix/v3/vms/list'
    payload = '{"kind":"vm"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    if int(json_data['metadata']['total_matches']) < 28:
        PrintSeperator('Checking Amount of VMS..')
        print('Check NOK...')


    # -----------------------------------------
    # Check to see which version of Karbon is 2.2.1
    # -----------------------------------------
    

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP=clusterIP[:-2]+str(int(clusterIP[-2:])+2)

    # URL to be used
    URL='https://'+PCIP+':9440/lcm/v1.r0.b1/resources/entities/list'
    payload = '{"filter":"entity_model==Karbon"}'
    method = "POST"
    # Get the anwser json from the API call
    json_data = CheckURL(URL, username, passwd,payload,method)
    KarbonVersion=json_data['data']['entities'][0]['version']
    if KarbonVersion != "2.2.1":
        PrintSeperator('Checking Karbon version..')
        print('Check NOK... version '+KarbonVersion+' is detected')
        print('Starting countermeasure.....')
        
        # Get the uuid of Karbon
        karbon_uuid=json_data['data']['entities'][0]['uuid']
        
        # Start the upgrade plan 
        URL='https://'+PCIP+':9440/lcm/v1.r0.b1/resources/notifications'
        payload='[{"version":"2.2.1","entity_uuid":"'+karbon_uuid+'"}]'
        method = 'POST'
        json_data = CheckURL(URL, username, passwd,payload,method)
        if json_data['data']['upgrade_plan'][0]['to_version'] == '2.2.1': # Accepted?
            URL='https://'+PCIP+':9440/lcm/v1.r0.b1/operations/update'
            payload='{"entity_update_spec_list":[{"version":"2.2.1","entity_uuid":"'+karbon_uuid+'"}]}'
            method = 'POST'
            json_data = CheckURL(URL, username, passwd,payload,method)
            if json_data['data']['task_uuid'] != "": # We have recieved a task_uuid, so all good
                print('Countermeasure has started...')
                karbon_nok[PCIP]=json_data['data']['task_uuid']
                print("Checking later on cluster "+PCIP+" with job uuid "+karbon_nok[PCIP]+"... Moving on...")
    
    # -----------------------------------------
    # Check to see if Karbon image is there
    # -----------------------------------------

    # PRISM Central is 2 higher than the last octet of the ClusterIP
    PCIP = clusterIP[:-2] + str(int(clusterIP[-2:]) + 2)

    # URL to be used
    URL = 'https://' + PCIP + ':9440/karbon/acs/image/list'
    payload = ''
    method = "GET"
    json_data = CheckURL(URL, username, passwd, payload, method)
    if 'Error' in json_data:
        print("Unable to connect to "+PCIP)
        return
    if len(json_data) < 1:
        return_code = openkarbon_ui(PCIP, username, passwd)
        if return_code == "Fail":
            return

    URL = 'https://' + PCIP + ':9440/karbon/acs/image/list'
    payload = ''
    method = "GET"
    json_data = CheckURL(URL, username, passwd, payload, method)
    if json_data['image_uuid'] == "":  # we don't have a karbon image in the system
        PrintSeperator('Checking Karbon image available..')
        print('Check NOK... image is not detected')
        print('Starting counter measures...')
        # Get the UUID of the image to be downloaded
        image_uuid = json_data['uuid']
        # Now start the download
        URL = 'https://' + PCIP + ':9440/karbon/acs/image/download'
        payload = '{"uuid":"' + image_uuid + '"}'
        method = "POST"
        json_data = CheckURL(URL, username, passwd, payload, method)
        if json_data['image_uuid'] == "":
            print("Counter measurement have failed. Please use Karbon UI to rectify!..")
        else:
            print("Counter measurements have started... Progress is in the Karbon UI..")


########################################################
# Main Routine
########################################################
for IP in open('clusterIP.1.txt','r'):
   CheckRoutine(IP.strip())

# Do we have some Clusters that we need to check due to Karbon version mismatch?
if len(karbon_nok) > 0:
    for PCIP,uuid in karbon_nok.items():
        print("Checking cluster "+PCIP+" on its status for the Karbon Update")
        URL='https://'+PCIP+':9440/api/nutanix/v3/tasks/'+uuid
        payload=''
        method = 'GET'
        json_data = CheckURL(URL, username, passwd,payload,method)
        counter=0
        while json_data['status'] != "SUCCEEDED":
            if json_data['status'] != "FAILED":
                print('Still running the upgrade... Sleep 60 sec')
                time.sleep(60)
                counter += 1
            else:
                print('The upgrade job of Karbon Failed...')
                break
            if counter > 10:
                print('We tried 10 minutes, canceling...')
                break
            json_data = CheckURL(URL, username, passwd,payload,method)
                    
                