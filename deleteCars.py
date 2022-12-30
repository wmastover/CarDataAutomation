from firebase_admin import credentials, firestore


def deleteCarsFunc(filename, db):

    filename = filename.replace(".csv", "")
    make,model,year = filename.split(" ")

    docRef = (u"Makes/"+ make +"/Models/" + model + "/Years/" + year)
    
    #create reference for Cars
    collectionRef  = db.collection(docRef  + "/" + "Cars")

    docs = collectionRef.list_documents(page_size=20)
    
    for doc in docs: 
        doc.delete()
    
    db.document(docRef).delete()
        
