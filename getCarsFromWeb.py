from numpy import product
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By

import os
from selenium.webdriver.chrome.options import Options

#go through an autotrader search and get the   
def getCars(make, model, year, date):
        
        # Check whether the specified path exists or not
       

        fileName = (date + "/" + make + " " + model + " " + year + ".csv")
 
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("window-size=1400,1000")

        chromedriver = ChromeDriverManager().install()
        driver = webdriver.Chrome( chromedriver, options=chrome_options)

        driver.get("https://www.autotrader.co.uk/car-search?sort=relevance&postcode=tq122pu" + "&make=" + make + "&model=" + model + "&exclude-writeoff-categories=on" + "&year-from=" + year + "&year-to=" + year )
        time.sleep(5)

        iframe = driver.find_element(By.ID, "sp_message_iframe_687971")

        driver.switch_to.frame(iframe)
        Buttons = driver.find_elements(By.TAG_NAME, "button")

        for x in Buttons:
            if x.get_attribute("title") == "Accept All":
                x.click()
                
        time.sleep(5)
        
        done = False
        lines = []
        count = 0

        while done == False:
            time.sleep(5)
            productCards = driver.find_elements(By.CLASS_NAME, "search-page__result")
            
            for x in productCards:
                try:
                    link = x.find_element(By.CLASS_NAME, "listing-fpa-link").get_attribute("href").split("?")[0]
                    
                    imageLink = x.find_element(By.CLASS_NAME, "product-card-image__main-image").get_attribute("src")
                    
                    productCardInfo = x.find_element(By.CLASS_NAME, "product-card-content__car-info")
                    priceWrapper = productCardInfo.find_element(By.CLASS_NAME,"product-card-pricing__price")
                except:
                    print("error in section 1")

                try:
                    if priceWrapper.find_element(By.CLASS_NAME, "product-card-pricing__small-copy") != None: 
                        print("lease")
                except:
                    try:
                        price = priceWrapper.find_element(By.TAG_NAME,"span").text.replace(",", "").replace("£","")
                        keySpecs = x.find_element(By.CLASS_NAME, "listing-key-specs")
                        keySpecisList = keySpecs.find_elements(By.TAG_NAME, "li")
                        
                        year = keySpecisList[0].text[:4]
                        mileage = keySpecisList[2].text.replace(" miles", "").replace(",","")
                        engineSize = keySpecisList[3].text
                        transmission = keySpecisList[5].text
                        fuelType = keySpecisList[6].text
                        
                        valid = True

                        #check data values
                        if "PS"  in mileage:
                            print("milage error")
                            valid = False
                               
                        if "PS" in engineSize or "L" not in engineSize:  
                            print("enginesize error")    
                            valid = False

                        if transmission != "Manual" and transmission != "Automatic":
                            print("transmission erro")
                            valid = False
                            
                        if fuelType != "Petrol" and fuelType != "Diesel":
                            print("fuel error")
                            valid = False

                        if valid == True:
                            line = {"price": price, "mileage": mileage, "engineSize": engineSize, "transmission":  transmission, "fuelType": fuelType, "link": link, "imageLink": imageLink} 
                            lines.append(line)         

                    except:
                        print("error in section 2")
                
            try:
                driver.find_element(By.CLASS_NAME, "pagination--right__active").click()
                count = count + 1
                print("Going through page " + str(count))
            except:
                done= True
                #convert array of dicts to dataframe

                seen = set()
                newLines = []
                for d in lines:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        newLines.append(d)
                
                data = pd.DataFrame.from_dict(newLines, orient='columns', dtype=None, columns=None)
                
                #remove index column
                data.reset_index()

                #print dataframe to csv
                data.to_csv(fileName, sep=',', encoding='utf-8', index=False)
                driver.quit()
