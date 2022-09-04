import os
import time
from random import uniform

import requests
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()


def send_message(text: str):
    """Sends a message to the chat id specified in the .env file via the telegram bot

    Args:
        text (str): text to be sent

    Returns:
        request.response
    """
    url = f"https://api.telegram.org/bot{os.environ.get('TOKEN')}/sendMessage"
    parameters = {"chat_id": os.environ.get("CHAT_ID"), "text": text}
    return requests.post(url, parameters)


def log_in(driver):
    """Logs into the website using the credentials in the .env file

    Args:
        driver (selenium.webdriver): driver object to log in
    """

    # Clicking the first prompt, if there is one
    try:
        driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/button").click()
        time.sleep(uniform(2, 4))
    except:
        pass

    # Filling the user and password
    user_box = driver.find_element(By.NAME, "user[email]")
    user_box.send_keys(os.environ.get("USERNAME"))
    time.sleep(uniform(2, 4))

    password_box = driver.find_element(By.NAME, "user[password]")
    password_box.send_keys(os.environ.get("PASSWORD"))
    time.sleep(uniform(2, 4))

    # Clicking the checkbox
    driver.find_element(By.XPATH, '//*[@id="new_user"]/div[3]/label/div').click()
    time.sleep(uniform(1, 2.5))

    # Clicking 'Sign in'
    driver.find_element(By.XPATH, '//*[@id="new_user"]/p[1]/input').click()
    time.sleep(uniform(1, 2.5))

    # Waiting for the page to load.
    # 5 seconds may be ok for a computer, but it doesn't seem enougn for the Raspberry Pi 4.
    time.sleep(6)
