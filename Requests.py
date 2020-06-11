import requests
import json
from dict2xml import dict2xml as xmlify
import html
import hmac
import hashlib
import base64

#Set Variables
CustomerId = 'ebab41e1-dc5a-4dfa-aa05-5c900cb839e8'
APIUrl ='https://smartconnectschedule.azurewebsites.net/API'
email = ''
password = ''
#Not needed for all endpoints
mapKey = '364fde19-0748-4d10-886f-a95300a506c5'

#Encode Password
def PasswordEncode():
    encodedpass = (password + ':6clDgmNok3WtR8GKYW6N').encode('utf-8')
    digest = hmac.new(b'6clDgmNok3WtR8GKYW6N', msg=encodedpass, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode()
    
#Retrieve an auth token from the SmartConnect server
def GetToken():
    url = APIUrl + "/GetToken"

    params = {'email': email,
            'password': PasswordEncode(),
            'companyID': CustomerId}
    response = requests.post(url, params = params)

    return response.text.replace('"','')

#Response Message Handler for map runs
def MessageHandler(response):
        if response["Status"] == 0:
                print('Run Number ' + str(response["RunNumber"]) + ' of map ' + response["MapId"] + ' Completed successfully')
        else:
                print('Run Number ' + str(response["RunNumber"]) + ' of map ' + response["MapId"] + ' Completed Unsuccessfully \nErrors: \n' + html.unescape(response["Errors"]))

#Retrieve a list of maps setup in SmartConnect
def GetMapList():
    url = APIUrl + "/GetMapList"

    params = {'token': GetToken()}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params)

    #Format and print response
    print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))

#Return a list of columns that were mapped in the integration process of a particular process
def GetMappedMapColumns():
    url = APIUrl + "/GetMappedMapColumns"

    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params)

    print(response.text)

#Get all data from the currently defined data source of a map as an XML data set
def GetAllData():
    url = APIUrl + "/GetAllData"

    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/xml'}

    response = requests.post(url, headers=headers, params = params)

    print(html.unescape(response.text))

#Get all data from the currently defined data source of a map using global variables as filters
def GetAllDataWithVariables():
    url = APIUrl + "/GetAllDataWithVariables"
    variablset = [{"Key":"GBL_TEST","Value":"Test"}, {"Key":"GBL_TEST2","Value":"Test2"}]
    payload = json.dumps(variablset)
    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/json',
            'Accept': 'application/xml'}

    response = requests.post(url, headers=headers, params = params, data = payload)

    print(html.unescape(response.text))

#Run a map while providing an XML data table
def runmapdatatable():
    url = APIUrl + "/RunMapDataTableWithErrors"
    dataset = [{"PostingDate":"9/16/2018","Batch":"ETHA","DocumentNo":"Test001","AccountType":"G_L_Account","AccountNo":"20100","AccountDescription":"Accounts Payable","Amount":"50"},
            {"PostingDate":"9/16/2018","Batch":"ETHA","DocumentNo":"Test001","AccountType":"G_L_Account","AccountNo":"10500","AccountDescription":"Prepaid Rent","Amount":"60"}]

    payload = '<RequestData> \n' + xmlify(dataset, wrap="Table") + '\n</RequestData>'
    #print(payload)
    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/xml',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params, data = payload)
    res = json.loads(response.text)
    MessageHandler(res)

#Run a map while providing an XML data table
def runmapxml():
    url = APIUrl + "/runmapxml"

    #Sample Data Set as List
    dataset = [{"PostingDate":"9/16/2018","Batch":"ETHAN","DocumentNo":"Test001","AccountType":"G_L_Account","AccountNo":"20100","AccountDescription":"Accounts Payable","Amount":"50"},
            {"PostingDate":"9/16/2018","Batch":"ETHAN","DocumentNo":"Test001","AccountType":"G_L_Account","AccountNo":"10500","AccountDescription":"Prepaid Rent","Amount":"60"}]
    #Encode the XML payload
    XMLData = '<DataSet>\n' + xmlify(dataset, wrap="Table") + '\n</DataSet>'

    payload = '<RequestData>' + '\n<Xml>' + html.escape(XMLData) + '\n</Xml>'  + '\n</RequestData>'

    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'text/xml',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params, data = payload)
    res = json.loads(response.text)
    MessageHandler(res)

#Run a process with the currently defined data source in SmartConnect
def RunMap():
    url = APIUrl + "/runmap"

    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params)
    res = json.loads(response.text)
    MessageHandler(res)

#Run a process with the currently defined data source in SmartConnect and provide variables
def RunMapWithVariables():
    url = APIUrl + "/RunMapWithVariables"

    variablset = [{"Key":"GBL_TEST","Value":"Test"}, {"Key":"GBL_TEST2","Value":"Test2"}]
    payload = json.dumps(variablset)
    params = {'token': GetToken(),
            'mapKey': mapKey}
    headers = {'Content-Type': 'application/json',
            'Accept': 'application/json'}

    response = requests.post(url, headers=headers, params = params, data = payload)
    res = json.loads(response.text)
    MessageHandler(res)


GetMapList()