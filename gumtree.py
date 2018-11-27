# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:14:07 2018

@author: LN043-HB
"""
import pandas as pd
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class gumtree_upload(object):   
    
    def __init__(self,df,username,password,path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 8)
        self.df=df
        self.username=username
        self.password=password
        self.image_path=path
        
    def log_in(self):
        self.browser.get('https://www.gumtree.sg/login.html')
        email_input=self.wait.until(EC.element_to_be_clickable((By.NAME,'email')))
        email_input.send_keys(self.username)
        pwd_input=self.wait.until(EC.element_to_be_clickable((By.NAME,'password')))
        pwd_input.send_keys(self.password)
        login_button=self.wait.until(EC.element_to_be_clickable((By.ID,'login-button')))
        login_button.click()
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME,"q")))
        except:
            sys.exit('Unable to log in')
            
        
    def wait_and_click(self,text):
        button=self.wait.until(EC.element_to_be_clickable((By.XPATH,"//li[@class='nav-item ']//*[contains(text(), '{}')]".format(text))))
        self.browser.execute_script("arguments[0].click();", button)
    
    def sendtext(self,elementname, value):
        if (value=='') | (value==' '):
            return
        element = self.wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        element.send_keys(value)
    
    def selectvalue(self,elementname, value):
        if (value=='') | (value==' '):
            return
        select_item=self.wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        select = Select(select_item)
        select.select_by_visible_text(value)
    
    def fill_in_form(self,value):
        self.browser.get('https://www.gumtree.sg/post.html')
        self.wait_and_click('Jobs')
        self.wait_and_click('Ad-hoc / Part-time Jobs')
        self.wait_and_click(value['Category'])
        self.wait_and_click(value['Location 1'])
        self.wait_and_click(value['Location 2'])
        # Job type
        self.selectvalue('JobType', value['JobType'])
        # Company Name
        self.sendtext('CompanyName', value['CompanyName'])
        # Company Website
        self.sendtext('CompanyWebsite', value['CompanyWebsite'])
        # EA License Number
        self.sendtext('EALicenseNumber', value['EALicenseNumber'])
        # Education Level
        self.selectvalue('EducationLevel', value['EducationLevel'])
        # Title
        self.sendtext('Title', value['Title'])
        # Description
        self.browser.switch_to.frame("description-frame")
        element = self.browser.find_element_by_id('rte')
        element.click()
        element.send_keys(value['Body'])
        self.browser.switch_to.default_content()
        # Username
        #self.sendtext('UserName', value['UserName'])
        #self.sendtext('Email',value['Email'])
        self.browser.execute_script("document.getElementsByName('Phone')[0].style.display = 'block';")
        self.sendtext('Phone',str(value['Phone']))
        # Photo Upload
        self.browser.find_element_by_name('u').send_keys('{}/{}.jpg'.format(self.image_path,value['Image Name']))
        time.sleep(15)
        # Address
        self.sendtext('Address', value['Address'])
        # Submission
        submit_button=self.wait.until(EC.element_to_be_clickable((By.ID,'postSubmit')))
        self.browser.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="icon-gl-message-success"]')))
            print('Ads has been published successfully')
        except:
            print('Unsuccessful')
        self.browser.delete_all_cookies()
    def automated_process(self):
        for row,value in self.df.iterrows():
            print('Row {} is running...'.format(row),end=' ')
            self.log_in()
            self.fill_in_form(value)
        print('Finished')
        self.browser.close()
            
            
        