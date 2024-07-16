import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import constants 
import datetime

config = constants.DATABASE_CONFIG
passjson = config['passjson']
urldb = config['urldb']
cred= credentials.Certificate(passjson)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': urldb,
        'databaseAuthVariableOverride': {
            'uid': 'my-service-worker'
        }
    })

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
now = str(now)

ref = db.reference()
ref.set({
    'flashcard_group':{
        '10000001':{
            'id':'10000001',
            'name':"red",
            'status':'1',
            'lastdate':now
        }
    },
    'flashcard':{
        '1':{
            
        }
    }
})