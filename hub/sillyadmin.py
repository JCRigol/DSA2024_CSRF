from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

user = os.getenv('USERNAME')
passw = os.getenv('PASSWORD')

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.set_preference("general.useragent.override", "Automatic Admin UserAgent")
driver = webdriver.Firefox(options=options)

actions = 0

try:
    #Victim enters the website he has admin privileges of, site1
    driver.get('http://site1:5001')

    actions += 1
    print(actions)

    #Victim logs onto site1
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    submit = driver.find_element(By.NAME,'submit')

    username.send_keys(user)
    password.send_keys(passw)
    submit.click()

    time.sleep(10) #Wait for action to complete, just in case

    #Successful action
    actions += 1
    print(actions)

    #Victim doesn't wipe their session from their machine and logs onto site2
    driver.get('http://site2:5002')

    time.sleep(10) #Wait for action to complete, just in case

    #Successful action
    actions += 1
    print(actions)

    #Victim commits a vulnerable action on site2
    submit = driver.find_element(By.NAME,'submit')
    submit.click()

    #Successful action
    actions += 1
    print(actions)

except:
    print('error')

finally:
    #Victim closes their browser after unknowingly being part of an attack
    driver.quit()
