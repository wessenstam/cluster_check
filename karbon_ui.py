from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import requests
import json

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

########################################################
# Functions Part
########################################################
# Print some seperation lines
def PrintSeperator(module):
    if "10." in module:
        print("*" * 40)
        print('Checking the cluster ' + module + '...')
        print("*" * 40)
    else:
        print("-" * 40)
        print("Checking " + module)
        print("-" * 40)
    return

# Function for checking URLs
def CheckURL(URL,username,passwd,payload,method):
    if method=="GET":
        # Get the anwser from the URL
        headers = {"Content-Type": "application/json"}
        try:
            anwser=requests.get(URL,verify=False,auth=(username,passwd),timeout=15,headers=headers)
        except:
            return "Error"
    else:
        headers={"Content-Type": "application/json"}
        anwser = requests.post(URL, verify=False, auth=(username, passwd), timeout=15,data=payload,headers=headers)

    json_data=json.loads(anwser.text)
    return json_data


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

def CheckRoutine(clusterIP):

    ########################################################
    PrintSeperator(clusterIP)
    ########################################################
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
    if json_data[0]['image_uuid'] == "":  # we don't have a karbon image in the system
        PrintSeperator('Checking Karbon image available..')
        print('Check NOK... image is not detected')
        print('Starting counter measures...')
        # Get the UUID of the image to be downloaded
        image_uuid = json_data[0]['uuid']
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