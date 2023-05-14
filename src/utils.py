import logging
import os
import time
from random import uniform

import requests
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()


def send_message(message: str):
    """Sends a message to the chat id specified in the .env file via the telegram bot

    Args:
        message (str): text to be sent

    Returns:
        request.response
    """
    url = f"https://api.telegram.org/bot{os.environ.get('TOKEN')}/sendMessage?chat_id={os.environ.get('CHAT_ID')}&text={message}"
    return requests.get(url)


def log_in(driver):
    """Logs into the website using the credentials in the .env file

    Args:
        driver (selenium.webdriver): driver object to log in
    """

    # Clicking the first prompt, if there is one
    try:
        driver.find_element(By.XPATH, "/html/body/div[7]/div[3]/div/button").click()
        logging.info("Bypassed the Log-in prompt successfully.")
        time.sleep(uniform(2, 4))
    except:
        logging.info(
            "Bypassed the Log-in prompt failed, HTML contents might have changed."
        )
        pass

    # Filling the user and password
    driver.find_element(By.NAME, "user[email]").send_keys(os.environ.get("USERNAME"))
    time.sleep(uniform(2, 4))

    driver.find_element(By.NAME, "user[password]").send_keys(os.environ.get("PASSWORD"))
    time.sleep(uniform(2, 4))

    # Clicking the checkbox
    driver.find_element(
        By.XPATH, "/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div"
    ).click()
    time.sleep(uniform(1, 2.5))

    # Clicking 'Sign in'
    driver.find_element(
        By.XPATH, "/html/body/div[5]/main/div[3]/div/div[1]/div/form/p[1]/input"
    ).click()

    # Waiting for the page to load.
    # 5 seconds may be ok for a computer, but it doesn't seem enougn for the Raspberry Pi 4.
    time.sleep(uniform(4, 7))
