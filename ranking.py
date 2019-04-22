from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
#import requests
import pyautogui
import os


options = Options()
options.set_headless(headless=True)
chromedriver = "/Users/Karan/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver, chrome_options=options)
#browser = webdriver.Chrome()#firefox_options=options)
url = 'https://results.nitrr.ac.in/Default.aspx'
browser.get(url)

results = []

for i in range(1,85):
	try:
		
		add = '0' + str(i)
		# if i > 88:
		# 	add = '90' + str(i-88)
		if i < 10:
			add = '00'+str(i)
		input_roll = browser.find_element_by_id("txtRegno")
		roll = '15119' + add
		print(roll)
		input_roll.clear()
		input_roll.send_keys(roll)

		show = browser.find_element_by_id("btnimgShow")
		show.click()

		select_element = Select(browser.find_element_by_id("ddlSemester"))
		select_element.select_by_value('7')

		showRes = browser.find_element_by_id("btnimgShowResult")
		showRes.click()

		name = browser.find_element_by_id("lblStudentName").text
		spi = browser.find_element_by_id("lblCPI").text
		print(f'{name} --> {spi}')
		results.append([name,float(spi)])
	except:
		print('exception occured')
		pass

print('RANKING')
results.sort(key=lambda x: x[1], reverse=True)
with open('cpi.txt', 'w') as f:
	i = 1
	for item in results:
		f.write(f"{i}. {item[0]} -- {item[1]}\n")
		i += 1
browser.quit()