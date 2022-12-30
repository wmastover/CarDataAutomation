#this file will run in each make / model folder.
#For each year, it will go through data files, remove duplicates, and output a trend
#line equation,
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import re

##change import file to use pandas to avoid error reading csv


def getTrendLineParamsFunc(carDataDicts):
        
    
    # initalise arrays to store mileage and price for all records in the file
    miles = []
    price = []

    #go through each record in the file and add to mile / price arrays
    for line in carDataDicts:
        
        try:
            miles.append(int(line.get("mileage")))
            price.append(int(line.get("price")))
            # print(line.get("Price"))
            # print(re.sub(r'[^0-9]', '', line.get("Price")))
            

        except:
            print("error with line:")
            print(line)

    #declare function of exponential trend line
    def func(x, a, b, ):
        return (a * np.exp(-b * x))
 
    #curve fit to data, popt is the array storing the optimum values of a and b
    popt, pcov = curve_fit(func, miles, price, p0=[10000, 0.0005])

    # print("Parameter a: " + str(popt[0]))  
    # print("Parameter b: " + str(popt[1]))
    

    #generate trendline data points
    price2 = []
    for i in miles:
       price2.append(func(i, popt[0], popt[1]))
    
    #show graph with data points and trendline
    # plt.plot(miles, price, "ko")
    # plt.plot(miles, price2, "ko", color="green") 
    # plt.show()
    numberOfDataPoints = len(miles)

    return(popt[0], popt[1], numberOfDataPoints )
