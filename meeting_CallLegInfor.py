import requests
import json
import pprint
import csv
from datetime import datetime,timezone
import pprint


def getMeetingInfor(vmrNumber):
    urlBase='https://p1.manage.vmr.telstra.com/callLegs/vmr/'
    url=urlBase + vmrNumber
    res = requests.get(url,stream=True)
    resContent=json.loads((res.content.decode('utf-8')))
    pprint.pprint(resContent)

    callId_callLegs={}

    for eachCallLeg in resContent:
        if eachCallLeg['callId'] in callId_callLegs:
            callId_callLegs[eachCallLeg['callId']].append(eachCallLeg)
        else:
            callId_callLegs[eachCallLeg['callId']]=[eachCallLeg]

    pprint.pprint(callId_callLegs)
    return(callId_callLegs)


def saveResultTOCsV(callId_callLegs,requiredFields):
    with open('meeting_callLegs.csv','w',newline='') as fileHanlder:
        csvFileHandler=csv.DictWriter(fileHanlder,fieldnames=requiredFields)
        csvFileHandler.writeheader()
        for eachMeeting in callId_callLegs.values():
            for eachLeg in eachMeeting:
                if eachLeg.get('startTime'):
                    callLegStartTimeUTC = eachLeg.get('startTime')
                    callLegStartTimeUTC = datetime.strptime(callLegStartTimeUTC, '%Y-%m-%dT%H:%M:%SZ')
                    callLegStartTimeLocal=callLegStartTimeUTC.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    eachLeg['startTime']=callLegStartTimeLocal

                requiredInfor={k:v for k,v in eachLeg.items() if k in requiredFields}
                csvFileHandler.writerow(requiredInfor)

if __name__=='__main__':
    requiredFields='vmrNumber,callId,startTime,duration,id,participantId,participantName,host,remoteAddress,status,cmsIp'.split(',')
    print( requiredFields)


    res=getMeetingInfor('+61874260001')
    saveResultTOCsV(res,requiredFields)

