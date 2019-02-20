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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class gumtree_upload(object):   
    
    # Initiate browser & define wait time, username, password and image path 
    def __init__(self,df,username,password,path):
        self.df=df
        self.username=username
        self.password=password
        self.image_path=path
    
    # Log into gumtree to avoid activation    
    def log_in(self):
        try:
            self.browser.close()
        except:
            pass
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 8)
        self.browser.get('https://www.gumtree.sg/login.html')
        email_input=self.wait.until(EC.element_to_be_clickable((By.NAME,'email')))
        email_input.send_keys(self.username)
        pwd_input=self.wait.until(EC.element_to_be_clickable((By.NAME,'password')))
        pwd_input.send_keys(self.password)
        login_button=self.wait.until(EC.element_to_be_clickable((By.ID,'login-button')))
        login_button.click()
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME,"q")))
            print('Log in sucessfully...',end=' ')
        except:
            sys.exit('Unable to log in')
    
    def delete_same_ads(self, value):
        self.browser.get('https://www.gumtree.sg/my/ads.html?ad=at')
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')))
        except:
            print('No ads has been posted in your list',end='...')
            return
        check=0
        while True:
            ads=self.browser.find_elements_by_xpath(
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')
            for ad in ads:
                if value['Title']==ad.find_element_by_class_name('title').text:
                    ad.find_element_by_class_name('delete').click()
                    self.browser.switch_to_alert().accept()
                    check=1
                    print('The same ad has been removed',end='...')
                    time.sleep(3)
                    break
            next_page=len(self.browser.find_elements_by_xpath('//a[@class="next follows"]'))
            if (next_page==0) | (check==1):
                break
            elif next_page!=0:
                next_page[0].click()
                self.wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')))
        if check==0:
            print('No same ad was found',end='...')
            
    def activate_new_ad(self):
        self.browser.get('https://www.gumtree.sg/my/ads.html?ad=at')
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')))
        except:
            print('No ads is pending',end='...')
            return
        ad=self.browser.find_element_by_xpath(
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')
        edit_button=ad.find_element_by_class_name('edit')
        edit_button.click()
        submit_button=self.wait.until(EC.element_to_be_clickable((By.ID,'postSubmit')))
        submit_button.click()
        
    # wait element to appear and click on it 
    def wait_and_click(self,text):
        self.error_column=text
        button=self.wait.until(EC.element_to_be_clickable((By.XPATH,
            "//li[@class='nav-item ']//*[contains(text(), '{}')]".format(text))))
        self.browser.execute_script("arguments[0].click();", button)

        
    # Wait textbox to appear and send inputs
    def sendtext(self,elementname, value):
        if (value=='') | (value==' '):
            return
        element = self.wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        element.send_keys(value)
    
    # Wait dropdown list to appear and select items
    def selectvalue(self,elementname, value):
        if (value=='') | (value==' '):
            return
        select_item=self.wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        select = Select(select_item)
        select.select_by_visible_text(value)
    
    # Fill in ads form and submit 
    def fill_in_form(self,value):
        try:
            self.browser.get('https://www.gumtree.sg/post.html')
            self.error_column=''
            self.wait_and_click('Jobs')
            self.wait_and_click('Ad-hoc / Part-time Jobs')
            self.wait_and_click(value['Category'])
            self.wait_and_click(value['Location 1'])
            self.wait_and_click(value['Location 2'])
            self.error_column=''
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
            '''
            self.wait.until(EC.presence_of_element_located((By.ID, "description-frame")))
                #self.browser.switchTo().frame("description-frame")
                self.browser.switch_to.frame("description-frame")
            except:
                self.browser.save_screenshot('screenshot.png')
                return 
            element = self.browser.find_element_by_id('rte')
            element.click()
            element.send_keys(value['Body'])
            self.browser.switch_to.default_content()
            '''
            self.browser.switch_to.frame("description-frame")
            element = self.browser.find_element_by_id('rte')
            element.click()
            element.send_keys(value['Body'])
            self.browser.switch_to.default_content()
            #self.sendtext('Description',value['Body'])
            # Username
            #self.sendtext('UserName', value['UserName'])
            #self.sendtext('Email',value['Email'])
            
            # Phone Number
            self.browser.execute_script("document.getElementsByName('Phone')[0].style.display = 'block';")
            self.sendtext('Phone',str(value['Phone']))
            # Photo Upload
            image_upload=self.browser.find_element_by_name('u')
            self.browser.execute_script("arguments[0].removeAttribute('multiple')",image_upload)
            image_upload.send_keys('{}/{}.jpg'.format(self.image_path,value['Image Name']))
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
                time.sleep(5)
            except:
                print('An error occurred during submission')
            # Clear cookies to avoid pre-settings of job location 
        except:
            if self.error_column=='':
                print('An unexpected error occurred.')
            else:
                print('An error occurred, wrong input:{}'.format(self.error_column))
            return 
        
    # Loop all the rows
    def automated_process(self):
        for row,value in self.df.iterrows():
            print('Row {} is running...'.format(row+1),end=' ')
            self.log_in()
            self.delete_same_ads(value)
            self.fill_in_form(value)
            self.activate_new_ad()
        print('Finished')
        self.browser.close()
            
            
        