# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:44:41 2019

@author: LN043-HB
"""

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

username='lhsjj0109@yeah.net'
password='lhs960109'

df=pd.read_excel('excel/Gumtree_Template_HS.xlsx')
value=df.iloc[1]
image_path='C:\\Users\\LN043-HB\\Pictures'
value['Image Name']='mooncake'
class gumtree_upload(object):   
    
    # Initiate browser & define wait time, username, password and image path 
    def __init__(df,username,password,path):
        df=df
        username=username
        password=password
        image_path=path
    
    # Log into gumtree to avoid activation    
    def log_in():
        try:
            browser.close()
        except:
            pass
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--start-maximized")
        browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
        wait = WebDriverWait(browser, 8)
        browser.get('https://www.gumtree.sg/login.html')
        email_input=wait.until(EC.element_to_be_clickable((By.NAME,'email')))
        email_input.send_keys(username)
        pwd_input=wait.until(EC.element_to_be_clickable((By.NAME,'password')))
        pwd_input.send_keys(password)
        login_button=wait.until(EC.element_to_be_clickable((By.ID,'login-button')))
        login_button.click()
        try:
            wait.until(EC.element_to_be_clickable((By.NAME,"q")))
            print('Log in sucessfully...',end=' ')
        except:
            sys.exit('Unable to log in')
    
    def delete_same_ads(value):
        browser.get('https://www.gumtree.sg/my/ads.html')
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')))
        except:
            print('No ads has been posted in your list',end='...')
          
        check=0
        while True:
            ads=browser.find_elements_by_xpath(
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')
            for ad in ads:
                if value['Title']==ad.find_element_by_class_name('title').text:
                    ad.find_element_by_class_name('delete').click()
                    browser.switch_to_alert().accept()
                    check=1
                    print('The same ad has been removed',end='...')
                    time.sleep(3)
                    break
            next_page=len(browser.find_elements_by_xpath('//a[@class="next follows"]'))
            if (next_page==0) | (check==1):
                break
            elif next_page!=0:
                next_page[0].click()
                wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class,"commercial") and contains(@class,"clearfix")]')))
        if check==0:
            print('No same ad was found',end='...')

    # wait element to appear and click on it 
    def wait_and_click(text):
        error_column=text
        button=wait.until(EC.element_to_be_clickable((By.XPATH,
            "//li[@class='nav-item ']//*[contains(text(), '{}')]".format(text))))
        browser.execute_script("arguments[0].click();", button)

        
    # Wait textbox to appear and send inputs
    def sendtext(elementname, value):
        if (value=='') | (value==' ') | pd.isnull(value):
            return
        element = wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        browser.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        element.send_keys(value)
    
    # Wait dropdown list to appear and select items
    def selectvalue(elementname, value):
        if (value=='') | (value==' '):
            return
        select_item=wait.until(EC.element_to_be_clickable((By.NAME,elementname)))
        select = Select(select_item)
        select.select_by_visible_text(value)
    
    # Fill in ads form and submit 
    def fill_in_form(value):
        try:
            browser.get('https://www.gumtree.sg/post.html')
            error_column=''
            wait_and_click('Jobs')
            wait_and_click('Ad-hoc / Part-time Jobs')
            wait_and_click(value['Category'])
            wait_and_click(value['Location 1'])
            wait_and_click(value['Location 2'])
            # Job type
            selectvalue('JobType', value['JobType'])
            # Company Name
            sendtext('CompanyName', value['CompanyName'])
            # Company Website
            sendtext('CompanyWebsite', value['CompanyWebsite'])
            # EA License Number
            sendtext('EALicenseNumber', value['EALicenseNumber'])
            # Education Level
            selectvalue('EducationLevel', value['EducationLevel'])
            # Title
            sendtext('Title', value['Title'])
            # Description
            '''
            wait.until(EC.presence_of_element_located((By.ID, "description-frame")))
                #browser.switchTo().frame("description-frame")
                browser.switch_to.frame("description-frame")
            except:
                browser.save_screenshot('screenshot.png')
                return 
            element = browser.find_element_by_id('rte')
            element.click()
            element.send_keys(value['Body'])
            browser.switch_to.default_content()
            '''
            browser.switch_to.frame("description-frame")
            element = browser.find_element_by_id('rte')
            element.click()
            element.send_keys(value['Body'])
            browser.switch_to.default_content()
            # Username
            #sendtext('UserName', value['UserName'])
            #sendtext('Email',value['Email'])
            
            # Phone Number
            browser.execute_script("document.getElementsByName('Phone')[0].style.display = 'block';")
            sendtext('Phone',str(value['Phone']))
            # Photo Upload
            image_upload=browser.find_element_by_id('pictures')
            browser.execute_script("arguments[0].removeAttribute('multiple')",image_upload)
            image_upload.send_keys('{}/{}.png'.format(image_path,value['Image Name']))
            time.sleep(15)
            browser.execute_script("arguments[0].scrollIntoView();", image_upload)
            browser.save_screenshot('1.png')
            #browser.execute_script("document.getElementById('loading').style.display = 'none';")
            # Address
            sendtext('Address', value['Address'])
            # Submission
            submit_button=wait.until(EC.element_to_be_clickable((By.ID,'postSubmit')))
            browser.execute_script("arguments[0].scrollIntoView();", submit_button)
            submit_button.click()
            try:
                wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="icon-gl-message-success"]')))
                print('Ads has been published successfully')
                time.sleep(8)
            except:
                print('An error occurred during submission')
            # Clear cookies to avoid pre-settings of job location 
        except:
            if error_column=='':
                print('An unexpected error occurred.')
            else:
                print('An error occurred, wrong input:{}'.format(error_column))
            return 
    # Loop all the rows
    def automated_process():
        for row,value in df.iterrows():
            print('Row {} is running...'.format(row+1),end=' ')
            log_in()
            delete_same_ads(value)
            fill_in_form(value)
        print('Finished')
        browser.close()
            
            
        