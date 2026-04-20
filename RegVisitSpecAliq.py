import requests
import json
from datetime import datetime, timezone
 
BASE_URL   = "https://test.openspecimen.org/rest/ng"
LOGIN_NAME = "Login Name"
PASSWORD   = "Password"
DOMAIN     = "openspecimen"
CP_ID      = 62
SITE_NAME  = "Monash Health Center"   
 
 
def post(session, path, payload):  #wrapper banaya hai to make repetitive things easier 
    resp = session.post(BASE_URL + path, json=payload)
    data = resp.json()
    if resp.status_code not in (200, 201):
        print(f"ERROR {resp.status_code}:", json.dumps(data, indent=2))
        raise SystemExit(1)
    return data
 
 
session = requests.Session()   # creates a session object - better than individual requests qki it will remember headers & cookies (mem id helps to rem across mul req) across calls
session.headers.update({"Content-Type": "application/json"})
 
auth = session.post(f"{BASE_URL}/sessions", json={
    "loginName": LOGIN_NAME,
    "password":  PASSWORD,
    "domain":    DOMAIN
}).json()
 
session.headers.update({"X-OS-API-TOKEN": auth["token"]})
print(f" Authenticated — token: {auth['token'][:20]}...")
print(" ")


cpr = post(session, "/collection-protocol-registrations/", {
    "participant" :{
        "firstName" : "Pratik",
        "lastName":"Patil",
        "emailAddress":"pratik05@gmail.com",
        "gender": "Male",
        "birthDate":"2005-03-14",
        "vitalStatus":"Alive",
        "races":["Asian"]
    },
    "cpId": CP_ID,
    "registrationDate":datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "dataEntryStatus":"COMPLETE"
})

cpr_id = cpr["id"]
print(f" Participant Registered — cprId: {cpr_id}")
print(" ")


visit = post(session,"/visits",{
    "cprId":cpr_id,
    "site":SITE_NAME,
    "name":"",
    "clinicalStatus":"Operative",
    "clinicalDiagnosis":["Leg Fracture"],
    "visitDate":"2026-04-21",
    "activityStatus":"Active",
    "dataEntryStatus":"COMPLETE"
})

visit_id = visit["id"]
print(f" Visit Created for Newly Registered Participant - visitId: {visit_id}")
print(" ")

now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

specimen = post(session,"/specimens", {
    "lineage":"New",
    "visitId": visit_id,
    "status":"Collected",
    "initialQty":"10",
    "availableQty":"10",
    "creationDate":"2026-04-21",
    "specimenClass":"Fluid",
    "type":"Bone Marrow Plasma",
    "pathology":"Non-Malignant, Diseased",
    "storageLocation": {},
    
    "collectionEvent": {
        "user":{
            "firstName":"staff first name",
            "lastName":"staff last name",
            "loginName":LOGIN_NAME,
            "emailAddress":"staff email",
            "domain":DOMAIN
        },
        "time":now_utc,
        "container":"Not Specified",
        "procedure":"Not Specified"
    },
    
    "receivedEvent":{
        "user":{
            "firstName":"staff first name",
            "lastName":"staff last name",
            "loginName":LOGIN_NAME,
            "emailAddress":"staff email",
            "domain":DOMAIN
        },
        "time":now_utc,
        "receivedQuality":"Acceptable"
    }
    
})

specimen_id = specimen["id"]
print(f" Primary Specimen Created - specimenId:{specimen_id}")

aliquots_list = []
for i in range(1,6):
    aliquots_list.append({
        "lineage":"Aliquot",
        "status":"Collected",
        "visitId":visit_id,
        "parentId":specimen_id,
        "initialQty":"2",
        "specimenClass":"Fluid",
        "createdOn":now_utc,
        "type":"Bone Marrow Plasma",
        "label":f"",
        "storageLocation":{}
    })
    
aliquots = post(session,"/specimens/collect",aliquots_list)
print(f" {len(aliquots_list)} Aliquots Created From Primary Specimen ")
print(" ")

for i in aliquots:
    print(f" id - {i["id"]} Label - {i["label"]} Qty - {i["initialQty"]}ml")
