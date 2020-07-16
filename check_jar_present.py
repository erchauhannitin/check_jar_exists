from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET
import time
import smtplib
from datetime import datetime
from time import strftime

URL = 'https://username:password@site/artifactory/'
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3454.26 Safari/537.36'}

def check_publish():
        time.sleep(3)
        
        try:
            page = requests.get(URL, headers=headers)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:  
            print('Exception occured, failed to reach path. Check connectivity to Host///')
            raise SystemExit(e)

        tree = html.fromstring(page.content)
        menu_versions = tree.xpath('/html/body/pre[2]/a')
        menu_dates = tree.xpath('/html/body/pre[2]/text()')

        found = False
        currentDay = str(datetime.now().day)
        currentMonth = str(datetime.now().month)
        currentYear = str(datetime.now().year)

        currentMonthName = strftime('%b')
        
        for i in range(60,len(menu_versions)): 
            menu_version = menu_versions[i].text
            if menu_version.startswith('6.0.0-rc8/'):           
                menu_date = menu_dates[i]  

                date_str = str(menu_date).strip()
                while currentYear in date_str and currentMonthName in date_str:
                    found = True
                    print('Entry found from April 2020')
                    print(date_str)
                    send_mail()
                    break
            
        if not found:
            print('No latest entry found at ' + datetime.now().strftime("%H:%M:%S"))           

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('bornfree.nitin@gmail.com', 'mhlmwndbswyusipk')

    subject = 'New version has been published for menu'
    body = 'Check Link '
    msg = f"Subject : {subject}\n\n{body}"

    server.sendmail(
        'bornfree.nitin@gmail.com',
        'nitin.c.chauhan@ericsson.com',
        msg
    )
    print('Mail has been Sent')
    server.quit

while(True):
    check_publish()
    time.sleep(60*10)
check_publish()
