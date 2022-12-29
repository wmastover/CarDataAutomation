import pandas as pd
from getGetCarsFromWeb import getCars

data = pd.read_csv("carsToCollect.csv",  engine='python')
data_dict = data.to_dict(orient="records")



for x in data_dict:
    make = x.get("Make")
    model = x.get("Model")

    print(make, model)
    x = 2005

    #run get cars function for all years of each model
    while x < 2021:
        getCars(make, model, str(x))
        x = x + 1