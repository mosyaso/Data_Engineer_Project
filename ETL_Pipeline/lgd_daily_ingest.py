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

tbeServerIp = "172.30.10.50"
tbeServerName = "TBE"
tbeServerUser = "pidemo"  #pidemo only

tbpServerIp = "172.30.10.105"
tbpServerName = "TBP"
tbpServerUser = "pidemo" #pidemo and piuser

pppServerIp = "192.168.201.8"
pppServerName = "PPP"
pppServerUser = "pidemo" #pidemo only

sevServerIp = "192.168.1.88"
sevServerName = "SEV"
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
    tbe_tag = "TBE.U40BAT1XCE031_XQ50"
    tbe_value = get_tag_lastvalue(tbe_tag)

    connect_to_Server(pppServerIp, pppServerUser)
    ppp_tag = "1AGCI_B:SYS134.PNT"
    ppp_value = get_tag_lastvalue(ppp_tag)
    
    connect_to_Server(tbpServerIp, tbpServerUser)
    tbp_tag10 = "TBP.U10.10CGA20EA037XQ00.out"
    tbp_tag20 = "TBP.U20.20CGA20EA037XQ00.out"
    tbp_tag30 = "TBP.U30.30CGA20EA037XQ00.out"
    tbp_value10 = get_tag_lastvalue(tbp_tag10)
    tbp_value20 = get_tag_lastvalue(tbp_tag20)
    tbp_value30 = get_tag_lastvalue(tbp_tag30)

    # connect_to_Server(sevServerIp, sevServerUser)
    # sev_tag1 = "19ADA10CE904_XJ51"
    # sev_tag2 = "29ADA10CE904_XJ51"
    # sev_value1 = get_tag_lastvalue(sev_tag1)
    # sev_value2 = get_tag_lastvalue(sev_tag2)
    sev_value1 = 0
    sev_value2 = 0

    #Total Generation 

    plantName = ["TBE", "TBP", "PPP", "SEV"]
    cityName = ["Kukup", "Kukup", "Seberang Perai", "Lumut"]
    latitude = [1.3356717429816323, 1.334394459207965, 5.375879372501105, 4.391758944961649]
    longitude = [103.54243832017674, 103.53333520183257, 100.3739439649467, 100.58828799377798]
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
        # res = requests.post('https://api.powerbi.com/beta/805b860b-a33a-4e2f-ac69-e9b1c553eff5/datasets/f030eceb-0658-4e60-81d8-821beaa1d30f/rows?experience=power-bi&key=VcxV6l9FNYfyQLA8Vrd8m01Z2rvqNdz3coBew8yZswpdCzJ%2Fy4q2RkVvUlUwnIm9CYoMznIE7f%2B5PcIOnsfVUQ%3D%3D', data=json.dumps(json_data))
        # print(res.status_code)
        # res1 = requests.post('https://api.powerbi.com/beta/805b860b-a33a-4e2f-ac69-e9b1c553eff5/datasets/07af056c-8ff4-4086-b952-3007c491c403/rows?experience=power-bi&key=MrZL5%2BNd5FOJcRjvIaUjPQ%2BbjoSbdPDBZa0GM48mY5WCeiIxUY%2Bqd2vrMPFH3%2FZCHQshPtOtj3Ztn8oXLAZ5ZQ%3D%3D', data=json.dumps(json_data1))
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