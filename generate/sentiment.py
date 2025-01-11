from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import traceback
from selenium.webdriver.common.by import By 
import cv2
import urllib
import numpy as np

# selenium actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



# Specify the path to your local Edge WebDriver (msedgedriver)
driver_path = "./msedgedriver.exe"

# Set up the Service with the path to Edge WebDriver
service = Service(driver_path)

# Initialize the Edge WebDriver using the Service object
driver = webdriver.Edge(service=service)

# action controls
actions = ActionChains(driver) 

# dataset
dataset = open("./dataset/dataset.csv", "a")
dataset.close()
image_iteration = 1

skip_post_counter = 320

try:

    # 1 - LOGIN
    # -----------------
    # Open a webpage
    driver.get("https://www.instagram.com")

    # Send tab twice to navigate to sign in section
    actions.send_keys(Keys.TAB * 2).perform()

    # Credentials
    username = None #redacted
    password = None #redacted

    # send usernmae, tab, password, enter
    actions.send_keys(username).perform()

    actions.send_keys(Keys.TAB).perform()

    actions.send_keys(password).perform()

    actions.send_keys(Keys.ENTER).perform()

    # load
    time.sleep(10)
    # -----------------

    # 2 - Navigate to AFL page content
    # -----------------
    driver.get("https://www.instagram.com/afl/")

    # load
    time.sleep(5)

    # content is 15 tabs away
    actions.send_keys(Keys.TAB * 17).perform()

    actions.send_keys(Keys.ENTER).perform()

    time.sleep(1)

    while(1):

        if(image_iteration > skip_post_counter):
            try:
                # get img
                current_post_img = driver.find_elements(By.XPATH, '//article[@tabindex="-1"]//img')[0]
                img_src = current_post_img.get_attribute('src')

                # get date
                date_holder = driver.find_elements(By.XPATH, '//time')[0]
                date_text = date_holder.get_attribute('datetime')
                print("POST DATE: {}".format(date_text))

                # get post URL
                current_URL = driver.current_url
                print("URL: {}".format(current_URL))

                # Image src
                print("IMG SRC: {}".format(img_src))

                # Label the image and save it locally
                img_location = f'./dataset/images/{image_iteration:09}.png'
                
                dataset = open("./dataset/dataset.csv", "a")
                dataset.write("{},{},{}\n".format(date_text, current_URL, img_location))
                dataset.close()

            except Exception as e:
                print(traceback.format_exc())

            try:
                req = urllib.request.urlopen(img_src)
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1) # 'Load it as it is'
                cv2.imshow('current post', img)
                cv2.waitKey(1)
                cv2.imwrite(img_location, img)

            except Exception as e:
                print(e)
            
            time.sleep(1)

        actions.send_keys(Keys.ARROW_RIGHT).perform()
        image_iteration += 1

        time.sleep(1)
    
    # -----------------

except Exception as e:
    dataset.close()
    print(traceback.format_exc())
    driver.quit()


dataset.close()
driver.quit()