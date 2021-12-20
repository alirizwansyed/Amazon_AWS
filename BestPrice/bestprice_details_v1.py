from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import csv
from datetime import datetime
import os 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

URL=r'https://www.bestprice.in/bestprice/v/TradeOffersLink?q=:relevance'
filename=r"C:\users\anumulapellis\downloads\bestprice_result_trade_offers_20211219.csv"
driverpath = r"C:\ProgramData\Chromedriver\chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('useAutomationExtension', True) 
driver = webdriver.Chrome(executable_path=driverpath,chrome_options=chromeOptions)
driver.get(URL)
driver.maximize_window()

#number of search results
search_results=int(driver.find_element(By.ID, 'bindResultsCount').get_attribute("textContent"))

#title
print(driver.find_element(By.XPATH,'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/a/h3').get_attribute("textContent"))
#URL
print(driver.find_element(By.XPATH,'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/a').get_attribute("href"))
#Selling price
print(driver.find_element(By.XPATH,'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/div[1]/span[1]/span').get_attribute("textContent"))
#MRP
print(driver.find_element(By.XPATH,'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/div[1]/span[2]/s[2]').get_attribute("textContent"))

sno_lst=[]
title_lst=[]
url_lst=[]
sp_lst=[]
mrp_lst=[]
margin_lst=[]
margin_perc_lst=[]
slab_available_lst=[]
for i in range(1,(search_results)+1):
    try:
        print(i)   
        #title
        title=(WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/a/h3'))).get_attribute("textContent"))
        #URL
        url=(WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/a'))).get_attribute("href"))
        #Selling price
        sp=(WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/div[1]/span[1]/span'))).get_attribute("textContent"))
        #MRP
        mrp=(WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/div[1]/span[2]/s[2]'))).get_attribute("textContent"))     
        #slab prices available
        try:
            slab_available=(WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/div[2]'))).get_attribute("textContent"))     
            if "Slab prices available".lower() in slab_available.lower():
                slab_available=True
            else:
                slab_available=False
        except:
            slab_available=False
        # title=(driver.find_element(By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/a/h3').get_attribute("textContent"))
        # #URL
        # url=(driver.find_element(By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/a').get_attribute("href"))
        # #Selling price
        # sp=(driver.find_element(By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/div[1]/span[1]/span').get_attribute("textContent"))
        # #MRP
        # mrp=(driver.find_element(By.XPATH,f'/html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[{i}]/div[3]/div[1]/span[2]/s[2]').get_attribute("textContent"))
        sp_calc=round(float(sp.replace("₹","").replace(",","").strip(" ")),2)
        mrp_calc=round(float(mrp.replace("₹","").replace(",","").strip(" ")),2)
        sno_lst.append(i)
        title_lst.append(title)
        url_lst.append(url)
        slab_available_lst.append(slab_available)
        sp_lst.append(round(float(sp.replace("₹","").replace(",","").strip(" ")),2))
        mrp_lst.append(round(float(mrp.replace("₹","").replace(",","").strip(" ")),2))
        margin_lst.append(round(float(mrp.replace("₹","").replace(",","").strip(" "))-float(sp.replace("₹","").replace(",","").strip(" ")),2))
        margin_perc_lst.append(round((1-(float(sp.replace("₹","").replace(",","").strip(" "))/float(mrp.replace("₹","").replace(",","").strip(" ")))),2))
    except Exception as e:
        print(i,str(e))
    if i%15==0:
        body = driver.find_element_by_css_selector('body')
        # body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.CONTROL+Keys.END)
        body.send_keys(Keys.PAGE_UP)
        body.send_keys(Keys.PAGE_DOWN)
        df=pd.DataFrame()
        df["SNo"]=sno_lst
        df["Title"]=title_lst
        df["MRP"]=mrp_lst
        df["Selling Price"]=sp_lst
        df["Margin"]=margin_lst
        df["Margin %"]=margin_perc_lst
        df["Slab Available"]=slab_available_lst
        df["URL"]=url_lst
        df.to_csv(filename,index=False,quoting=csv.QUOTE_ALL)
df=pd.DataFrame()
df["SNo"]=sno_lst
df["Title"]=title_lst
df["MRP"]=mrp_lst
df["Selling Price"]=sp_lst
df["Margin"]=margin_lst
df["Margin %"]=margin_perc_lst
df["Slab Available"]=slab_available_lst
df["URL"]=url_lst
df.to_csv(filename,index=False,quoting=csv.QUOTE_ALL)
driver.close()

# title:-
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/a/h3
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[2]/div[3]/a/h3
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[41]/div[3]/a/h3
# url:-
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/a
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[2]/div[3]/a
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[41]/div[3]/a
# selling price:-
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/div[1]/span[1]/span
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[2]/div[3]/div[1]/span[1]/span
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[41]/div[3]/div[1]/span[1]/span
# MRP:-
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/div[1]/span[2]/s[2]
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[2]/div[3]/div[1]/span[2]/s[2]
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[41]/div[3]/div[1]/span[2]/s[2]
# Slab price:-
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/div[3]/div[2]
# /html/body/main/main/section/div/div/div[2]/div/div/div[1]/div[2]/div[4]/div[11]/div[3]/div[2]