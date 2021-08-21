from datetime import datetime as dt
import datetime
import os
import json
import dotenv
import firebase_admin
from firebase_admin import credentials,firestore

#dotenv.load_dotenv()
#key = json.loads(os.getenv("firebaseKey"))
#cred = credentials.Certificate(key)

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

currentSeason = 2 #change here

def add(name):
    if isValid() != 'OK':
        return "Duplicated date " + isValid()
    
    names = ['Tun','Ice','Fain','Pong','Palm','JJ']
    check = False
    for i in names:
        if i.lower() == name.lower() :
            check = True
            name = i

    if not check:
        return "Invalid name"

    now = str(dt.utcnow())
    collectionName = 'counter log s'+ str(currentSeason)
    firestore_db.collection(collectionName).add({'name':name,'date':now.split()[0],'time':now.split()[1]})
    print(f'add {name} to scoreboard successfully')
    return name

def getScore(season):
    print("open database:")
    if season == 1:
      name = 'counter log'
    else:
      name = 'counter log s'+ str(season)
    print(name)
    snapshots= [x.to_dict() for x in list(firestore_db.collection(name).get())]

    data = {'Tun':0,'Ice':0,'Fain':0,'Pong':0,'Palm':0,'JJ':0}

    for x in snapshots:
        data[x['name']] += 1
    
    return data
    
def listScore(season):
    data = getScore(season)
    output = []
    for i,j in data.items():
        if j != 0:
            output.append([j,i])

    if len(output) == 0:
        return "Empty"
    
    output.sort(reverse = True)
    output = [j+" "+str(i) for [i,j] in output]
    return '\n'.join(output)

def getLastScore():
    print("open database")
    collectionName = 'counter log s'+ str(currentSeason)
    snapshots = [x.to_dict() for x in list(firestore_db.collection(collectionName).get())]
    
    mxDate = dt.strptime(snapshots[0]['date'],"%Y-%m-%d")
    result = snapshots[0]

    for x in snapshots:
        if dt.strptime(x['date'],"%Y-%m-%d") > mxDate:
            mxDate = dt.strptime(x['date'],"%Y-%m-%d")
            result = x

    result['time'] = (dt.strptime(result['time'],"%H:%M:%S.%f") + datetime.timedelta(hours=7)).strftime("%H:%M:%S")
    return result 

def isValid():
    utc = dt.utcnow()
    print("Current time: ",utc)

    collectionName = 'counter log s'+ str(currentSeason)
    snapshots = [x.to_dict() for x in list(firestore_db.collection(collectionName).get())]
    for x in snapshots:
        if(x['date'] == str(utc).split()[0]):
            return x['name']
    return 'OK' 