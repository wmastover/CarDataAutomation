import pandas as pd
from getCarsFromWeb import getCars
import os
from getTrendlineParams import getTrendLineParamsFunc
from getBestCars import getBestCarsFunc
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from deleteCars import deleteCarsFunc 
from uploadCars import uploadCarsFunc

data = pd.read_csv("carsToCollect.csv",  engine='python')
data_dict = data.to_dict(orient="records")

date = datetime.today().strftime('%d%m%Y')
# run web scraper for each car / year in carsToCollect.csv
for x in data_dict:
    make = x.get("Make")
    model = x.get("Model")

    print(make, model)
    x = 2005

    #run get cars function for all years of each model
    while x < 2021:
        getCars(make, model, str(x), date)
        x = x + 1


# import credentials for firebase 
cwd = os.getcwd()
cred = credentials.Certificate(cwd + "/FirebaseCredentials.json")

# initialise firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

directory = os.fsencode(date)
#loop through each csv in the dated folder
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     print(filename)
     if filename.endswith(".csv"): 
        
        address = date + "/" + filename
        carData = pd.read_csv(address,  engine='python')
        carDataDicts = carData.to_dict(orient="records")
        

        #generate trendline params
        a,b, numberOfDataPoints = getTrendLineParamsFunc(carDataDicts)

        # print(a,b)
        
        #select the best 20 cars
        uploadList = getBestCarsFunc(carDataDicts, a, b)
            
        #delete firebase record for given car and year
        
        deleteCarsFunc(filename, db)

        #upload 20 best cars and trendline params 
        uploadCarsFunc(filename, uploadList, a, b, numberOfDataPoints, db)