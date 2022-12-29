from numpy import product
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import os
#go through an autotrader search and get the   
def getCars(make, model, year):
        date = datetime.today().strftime('%d%m%Y')

        path = date
# Check whether the specified path exists or not
        isExist = os.path.exists(path)
        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(path)

        fileName = (date + "/" + model + " " + year + ".csv")

        chromedriver = ChromeDriverManager().install()
        driver = webdriver.Chrome(chromedriver )

        driver.get("https://www.autotrader.co.uk/car-search?sort=relevance&postcode=tq122pu" + "&make=" + make + "&model=" + model + "&exclude-writeoff-categories=on" + "&year-from=" + year + "&year-to=" + year )
        time.sleep(5)

        iframe = driver.find_element(By.ID, "sp_message_iframe_687971")

        driver.switch_to.frame(iframe)
        Buttons = driver.find_elements(By.TAG_NAME, "button")

        for x in Buttons:
            if x.get_attribute("title") == "Accept All":
                x.click()
                
        time.sleep(5)
        count = 0
        done = False
        lines = []
        while done == False:
            time.sleep(5)
            productCards = driver.find_elements(By.CLASS_NAME, "search-page__result")
            
            

            for x in productCards:

                link = x.find_element(By.CLASS_NAME, "listing-fpa-link").get_attribute("href")
                
                imageLink = x.find_element(By.CLASS_NAME, "product-card-image__main-image").get_attribute("src")
                
                productCardInfo = x.find_element(By.CLASS_NAME, "product-card-content__car-info")
                priceWrapper = productCardInfo.find_element(By.CLASS_NAME,"product-card-pricing__price")

                try:
                    if priceWrapper.find_element(By.CLASS_NAME, "product-card-pricing__small-copy") != None: 
                        print("lease")
                except:
                    count = count + 1
                    price = priceWrapper.find_element(By.TAG_NAME,"span").text.replace(",", "")
                    keySpecs = x.find_element(By.CLASS_NAME, "listing-key-specs")
                    keySpecisList = keySpecs.find_elements(By.TAG_NAME, "li")
                    
                    year = keySpecisList[0].text[:4]
                    mileage = keySpecisList[2].text.replace(" miles", "").replace(",","")
                    engineSize = keySpecisList[3].text
                    transmission = keySpecisList[5].text
                    fuelType = keySpecisList[6].text
                    

                    print(price, year, mileage, engineSize, transmission, fuelType)
                    
                    line = {"price": price, "mileage": mileage, "engineSize": engineSize, "transmission":  transmission, "fuelType": fuelType, "link": link, "imageLink": imageLink }
                    lines.append(line)
            
            try:
                driver.find_element(By.CLASS_NAME, "pagination--right__active").click()
            except:
                done= True
                #convert array of dicts to dataframe
                print(lines)
                data = pd.DataFrame.from_dict(lines, orient='columns', dtype=None, columns=None)
                print(data)
                #remove index column
                data.reset_index()
                #print dataframe to csv
                print( count)
                data.to_csv(fileName, sep=',', encoding='utf-8', index=False)
                driver.close()

    
getCars("Ford","Fiesta", "2005")