
def uploadCarsFunc(filename, uploadList , a , b, numberOfDataPoints, db):

    filename = filename.replace(".csv", "")
    make,model,year = filename.split(" ")

    docRef = (u"Makes/"+ make +"/Models/" + model + "/Years/" + year)
    
    db.document(docRef).set({u'parameterA': a})    
    db.document(docRef).update({u'parameterB': b})
    db.document(docRef).update({u'numberOfDataPoints': numberOfDataPoints})

    #create reference for Cars
    collectionRef  = db.collection(docRef  + "/" + "Cars")

    list(map(lambda x: collectionRef.add(x), uploadList))