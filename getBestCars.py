import numpy as np
from operator import itemgetter

def getBestCarsFunc(carDataDicts, a, b):
    
    def func(x, a, b, ):
        return (a * np.exp(-b * x))
    
    def percentageDiscount(price, expectedPrice):
       return( (expectedPrice - price) / expectedPrice * 100)

    positiveDiscountCars = []

    for line in carDataDicts:
        
        try:
            miles = line.get("mileage")
            price = line.get("price")
            expectedPrice = int(func(miles, a, b))
            discount = int(percentageDiscount(price, expectedPrice))

            if discount > 0:
                line["expectedPrice"] = expectedPrice
                line["discount"] = discount

                positiveDiscountCars.append(line)
                #print(price, expectedPrice, discount)

        except:
            print("error with line:")
            print(line)
    

    
    sortedList = sorted(positiveDiscountCars, key=itemgetter("discount"), reverse=True)[:20]
    
    # for x in sortedList:
    #     print(x.get("expectedPrice"))
    #     print(x.get("discount"))

    print(len(sortedList))

    return(sortedList)