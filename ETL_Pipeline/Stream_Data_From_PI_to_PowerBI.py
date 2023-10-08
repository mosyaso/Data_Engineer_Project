import json
import requests
import sys
import os
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')
import time
import datetime
from datetime import datetime
import psutil
import pytz
import schedule

from OSIsoft.AF.PI import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from System.Net import NetworkCredential # by default by window

tbeServerIp = "xxx.xx.xx.xx"
tbeServerName = "XXX"
tbeServerUser = "pidemo"  #pidemo only

tbpServerIp = "xxx.xx.xx.xx"
tbpServerName = "XXX"
tbpServerUser = "pidemo" #pidemo and piuser

pppServerIp = "xxx.xx.xx.xx"
pppServerName = "XXX"
pppServerUser = "pidemo" #pidemo only

sevServerIp = "xxx.xx.xx.xx"
sevServerName = "XXX"
sevServerUser = "piuser" #pidemo and piuser

def connect_to_Server(serverName, serverUser):
    try:
        piServers = PIServers()
        global piServer
        piServer = piServers[serverName]
        # print(piServer)
        serverCred = NetworkCredential(serverUser, None)
        connection = piServer.Connect(serverCred)
        # print(piServer.ConnectionInfo.IsConnected)
    except Exception as e:
        print(e)
        return

def get_tag_lastvalue(tagname):
    try:
        tag = PIPoint.FindPIPoint(piServer, tagname)

        # last value 
        # like a CurrentValue() there are many more methods available on internet you can find
        #print("tagvalue",tag)

        last_value = tag.CurrentValue()
        #print("last_value",last_value)

        if type(last_value.Value) == float or type(last_value.Value) == int:
            previous_data = last_value.Value
            print("store previous data =", previous_data)
            return last_value.Value
        else:
            # return last_value.Value.Value
            print("display previous data")
            return previous_data

    except Exception as e:
        print(tagname, " --> ", e)
        return

def collect_data():
    
    connect_to_Server(tbeServerIp, tbeServerUser)
    tbe_tag = "XXXXXXX"
    tbe_value = get_tag_lastvalue(tbe_tag)

    connect_to_Server(pppServerIp, pppServerUser)
    ppp_tag = "XXXXXXX"
    ppp_value = get_tag_lastvalue(ppp_tag)
    
    connect_to_Server(tbpServerIp, tbpServerUser)
    tbp_tag10 = "XXXXXXX"
    tbp_tag20 = "XXXXXXX"
    tbp_tag30 = "XXXXXXX"
    tbp_value10 = get_tag_lastvalue(tbp_tag10)
    tbp_value20 = get_tag_lastvalue(tbp_tag20)
    tbp_value30 = get_tag_lastvalue(tbp_tag30)

    connect_to_Server(sevServerIp, sevServerUser)
    sev_tag1 = "XXXXXXX"
    sev_tag2 = "XXXXXXX"
    sev_value1 = get_tag_lastvalue(sev_tag1)
    sev_value2 = get_tag_lastvalue(sev_tag2)

    #Total Generation 

    plantName = ["XXX", "XXX", "XXX", "XXX"]
    cityName = ["XXX", "XXX", "XXX", "XXX"]
    latitude = [XXXX, XXXX, XXXX, XXXX]
    longitude = [XXXX, XXXX, XXXX, XXXX]
    powerGeneration1 = [tbe_value, tbp_value10, ppp_value, sev_value1]
    powerGeneration2 = [0, tbp_value20, 0, sev_value2]
    powerGeneration3 = [0, tbp_value30, 0, 0]
    
    json_data = []
    for i in range(len(plantName)):
        entry = {
            'timestamp': now,
            'plantName': plantName[i],
            'city': cityName[i],
            'latitude': latitude[i],
            'longitude': longitude[i],
            'powerGeneration1': powerGeneration1[i],
            'powerGeneration2': powerGeneration2[i],
            'powerGeneration3': powerGeneration3[i],
        }
        json_data.append(entry)

    json_data1 = [{
        'timestamp': now,
        'tbe_value': tbe_value,
        'ppp_value': ppp_value,
        'tbp_value10': tbp_value10,
        'tbp_value20': tbp_value20,
        'tbp_value30': tbp_value30,
        'sev_value1': sev_value1,
        'sev_value2': sev_value2,
        'totalGeneration': tbe_value + ppp_value + tbp_value10 + tbp_value20 + tbp_value30 + sev_value1 + sev_value2,
        'totalTBP': tbp_value10 + tbp_value20 + tbp_value30,
        'totalSEV': sev_value1 + sev_value2,
        'tbe_cf': (tbe_value/(1000*24))*100,
        'ppp_cf': (ppp_value/(341.17*24))*100,
        'tbp_cf': ((tbp_value10 + tbp_value20 + tbp_value30)/(2100*24))*100,
        'sev_cf': ((sev_value1 + sev_value2)/(1303*24))*100
    }]
        
    return json_data1

def record_data():
    data = collect_data()
    with open('lgd_daily_data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

schedule.every(15).minutes.at(":00").do(record_data)

while True:
    try:
        start_time = time.time()
        now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")
        res = requests.post('powerBI API', data=json.dumps(json_data))
        print(res.status_code)
        # res1 = requests.post('powerBI API', data=json.dumps(json_data1))
        # print(res1.status_code)
        # print(json_data)
        # print(json_data1)
        print(collect_data())
        schedule.run_pending()
        
        #time.sleep(5)
        sleep_time = time.time() - start_time
        print("time taken in seconds ", int(sleep_time))
        print("------------------------------------------------------------------------")
        if sleep_time < 30:
            time.sleep(30 - int(sleep_time))

    except Exception as e:
        print(f"An error occurred: {e}")
        continue
