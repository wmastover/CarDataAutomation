from firebase_admin import credentials, firestore


def deleteCars(make, model, year, db):
    databaseLocationString = (u"Makes/"+ make +"/Models/" + model + "/Years" )
    print(databaseLocationString)
    #create reference for car
    collectionRef  = db.collection(databaseLocationString  + "/" + year)