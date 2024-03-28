from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import time
import re
import sys

user_login = sys.argv[1]
user_passwd = sys.argv[2]


definitions = defaultdict(list)
examples = defaultdict(list)


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.etutor.pl/")

driver.implicitly_wait(10)

try:
    cookie_button = driver.find_element(By.ID, "AllCookiePolicyConfirmation")
    cookie_button.click()

    login_button = driver.find_element(By.XPATH, "//a[@href='/account/login']")
    login_button.click()

    login = driver.find_element(By.ID, "login")
    login.clear()
    login.send_keys(user_login)

    passwd = driver.find_element(By.ID, "haslo")
    passwd.clear()
    passwd.send_keys(user_passwd)

    confirm_button = driver.find_element(By.XPATH, '//button[contains(., "Zaloguj się")]')
    confirm_button.click()

    menu_icon = driver.find_element(By.ID, "thinHeaderMenuIcon")
    menu_icon.click()

    words_button = driver.find_element(By.XPATH, "//a[@href='/words']")
    words_button.click()

    user_words = driver.find_element(By.XPATH, "//a[@href='/words/user-words']")
    user_words.click()

    word_list = driver.find_elements(By.CLASS_NAME, "wordsListName")

    for index in range(len(word_list)):
        word_list = driver.find_elements(By.CLASS_NAME, "wordsListName")
        wl = word_list[index]
        numbers = re.findall(r'\d+', wl.text)
  
        length = int(numbers[-1])

        button = wl.find_element(By.CLASS_NAME, "listName")
        button.click()

        for i in range(1, length + 1):

            word = driver.find_element(By.ID, "element_" + str(i))

            # element = driver.find_element(By.CSS_SELECTOR, ".hws.phraseEntity")
            # ".klasa1, .klasa2" =>  jedną lub drugą klasę
            temp = word.text.split("\n= ")

            key = temp[0].split('\n')[0]
            data = temp[1].split('\n')

            definitions[key].append(data[0])

            if len(data) > 1:
                
                for i in range(1, len(data[1:]), 2):
                    examples[key].append((data[i], data[i + 1]))
        driver.back()
    
except Exception as e:
    print("Error:", e)

for key, value in definitions.items():
    print("Word: ", key)
    print("Definitions: ", value)
    print("Examples: ", examples[key])
    print()

import json

with open('definitions.json', 'w') as json_file:
    json.dump(definitions, json_file, indent=4)

with open('examples.json', 'w') as json_file:
    json.dump(examples, json_file, indent=4)