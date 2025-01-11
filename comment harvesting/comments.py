from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import traceback
from selenium.webdriver.common.by import By 
import cv2
import urllib
import numpy as np
from selenium.webdriver.edge.options import Options as EdgeOptions

# selenium actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Specify the path to your local Edge WebDriver (msedgedriver)
driver_path = "./msedgedriver.exe"

# Set up the Service with the path to Edge WebDriver
service = Service(driver_path)
# options = EdgeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize the Edge WebDriver using the Service object
driver = webdriver.Edge(service=service)

# action controls
actions = ActionChains(driver) 

comments_database = open("./comments.csv", "w", encoding="utf-8")
comments_database.close()

try:

    # 1 - LOGIN
    # -----------------
    # Open a webpage
    driver.get("https://www.instagram.com")

    time.sleep(2)

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

    # 2 - FIND RESULTS POSTS
    # -----------------
    # get the posts to hit
    posts_database = open("../dataset/dataset.csv", "r").read().split("\n")[:-1]
    results_posts_database = open("../post processing/results.txt", "r").read().split("\n")[:-1]
    

    for post in posts_database:
        post_data = post.split(",")
        post_date, post_link, post_image_location = post_data

        if post_image_location.split("/")[-1] in results_posts_database:
            # -----------------

            # 3 - load the post
            # -----------------
            print("RESULTS POST FOUND: {}".format(post_link))

            driver.get(post_link)

            # load
            time.sleep(3)
            # -----------------

            final_comment_list = []
            comment_list = []
            
            actions.send_keys(Keys.TAB * 12).perform()

            for i in range(0, 20):
                actions.send_keys(Keys.ARROW_DOWN * 30).perform()
                time.sleep(1)

                # get comments
                comments = driver.find_elements(By.XPATH, '//span[@style="----base-line-clamp-line-height: 18px; --lineHeight: 18px;"]')
                likes = driver.find_elements(By.XPATH, '//span[@style="----base-line-clamp-line-height: 16px; --lineHeight: 16px;"]')

                immediate_comment_list = []

                for comment in comments:
                    comment_text = comment.get_attribute("innerHTML")
                    
                    if((("<div" in comment_text and "=" in comment_text and "\"" in comment_text)) or ("•" == comment_text) or ("<time " in comment_text) or (("<a" in comment_text) and ("href" not in comment_text)) or ("</span> likes</span>" in comment_text)):
                        continue

                    if(comment_text not in comment_list):
                        comment_list.append(comment_text)
                
                # Could measure likes on comments, but i'm running out of time so omitting this for now... 
                # previous_content = None
                # immediate_likes_list = []
                # for like in likes:
                #     like_text = like.get_attribute("innerHTML")
                    
                #     if(" likes</span>" in like_text):
                #         like_text = like_text.split("\">")[-1].split("</s")[0]
                #         immediate_likes_list.append(like_text)
                    
                #     else:
                #         if(previous_content is not None):
                #             if(("Reply" in previous_content or "replies" in previous_content) and ("Reply</span>" in like_text)):
                #                 immediate_likes_list.append("0 likes")


                #     previous_content = like_text

            if("posts" in comment_list):
                comment_list.remove("posts")
            if("followers" in comment_list):
                comment_list.remove("followers")
            if("following" in comment_list):
                comment_list.remove("following")
                
            comments_database = open("./comments.csv", "a", encoding="utf-8")
            comments_database.write("{},".format(post_image_location))

            for comment in comment_list:
                comments_database.write("{}".format(comment))
                comments_database.write(";")

            comments_database.write("\n")
            comments_database.close()


except Exception as e:
    print(traceback.format_exc())
    driver.quit()


driver.quit()