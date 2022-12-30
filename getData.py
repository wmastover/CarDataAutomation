import pandas as pd
from getGetCarsFromWeb import getCars
import os
from datetime import datetime

data = pd.read_csv("carsToCollect.csv",  engine='python')
data_dict = data.to_dict(orient="records")


# run web scraper for each car / year in carsToCollect.csv
for x in data_dict:
    make = x.get("Make")
    model = x.get("Model")

    print(make, model)
    x = 2005

    #run get cars function for all years of each model
    while x < 2021:
        getCars(make, model, str(x))
        x = x + 1

date = datetime.today().strftime('%d%m%Y')
directory = os.fsencode(date)

#loop through each csv in the dated folder
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"): 
        
        address = date + "/" + filename
        carData = pd.read_csv(address,  engine='python')
        carDataDicts = carData.to_dict(orient="records")
        print(carDataDicts)
