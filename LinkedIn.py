
import csv

import openpyxl

import pandas as pd

from pandas import DataFrame

from parsel import Selector

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import requests,time,random

from bs4 import BeautifulSoup

Email = input("Enter your email ID")

Password = input("Enter your password")

keyword = input("Enter the designation : ")

Loc = input("Enter the location : ")

database = []

driver = webdriver.Chrome('/Users/Anirudh/Desktop/crawling/chromedriver')

driver.get("https://www.linkedin.com/login?") 

username = driver.find_element_by_name('session_key')

username.send_keys(Email)

password = driver.find_element_by_xpath('//*[@id="password"]')

password.send_keys(Password)

log_in_button = driver.find_element_by_class_name('btn__primary--large')

log_in_button.click()

driver.get('https://www.google.com/')

search_input = driver.find_element_by_name('q')

search_input.send_keys('site:linkedin.com/in/ AND ' + keyword + ' AND ' + Loc)

search_input.send_keys(Keys.RETURN)

a = driver.current_url

time.sleep(5)

while True:
   
    profile = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
    
    profile = [prof.get_attribute('href') for prof in profile]

    for prof in profile:
        
        driver.get(prof)
        
        time.sleep(5)
        
        try:
            
            sel = Selector(text=driver.page_source)
            
            name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
            
            job_title = sel.xpath('//*[@class="mt1 t-18 t-black t-normal break-words"]/text()').extract_first().strip()
            
            company = sel.xpath('//*[@class="text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view"]/text()').extract_first().strip()
            
            location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
                                           
            ln_url = driver.current_url
            
            temp = [name,job_title,company,location,ln_url]
            
            database.append(temp)
        
        except:
                print('failed')
    
    
    driver.get(a)
  
    Next_Google_page = driver.find_element_by_link_text("Next").click()
    
    time.sleep(5)
    
    a = driver.current_url

driver.quit()

database  

Profiles = pd.DataFrame(database,columns = ['Name','Designation','Company','Location','URL'])
Profiles

Profiles.to_excel('/Users/Anirudh/Desktop/data.xlsx')