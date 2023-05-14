import datetime
import json
import logging
import os
import time
from random import uniform

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from utils import log_in, send_message

load_dotenv()
URL = f"https://ais.usvisa-info.com/en-ca/niv/schedule/{os.environ.get('URL_ID')}/appointment"

LOG_PATH = "logs.txt"

logging.basicConfig(
    filename=LOG_PATH,
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

script_exec_dt = datetime.datetime.now()


# Setting Chrome options to run the scraper headless.
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
logging.info("Driver connected.")

# logging in
log_in(driver)
logging.info("User logged in successfully.")

action = ActionChains(driver)

# initialize availability dict
availability = {}

# get all locations from the dropdown
location_select = Select(
    driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
)
location_options = location_select.options[1:]

logging.info("Attempting to browse through the Location dropdown...")

for option in location_options:
    option.click()
    availability[option.text] = {}
    time.sleep(uniform(2, 4))

    # extract the datepicker element
    datepicker = driver.find_element(By.ID, "appointments_consulate_appointment_date")
    try:
        datepicker.click()
    except ElementNotInteractableException:
        logging.info(f"Datepicker not available in city: {option.text}")
        continue
    time.sleep(uniform(2, 4))

    # initialize a list to store the clickable dates (<a> tags)
    date_elements_list = []

    # how many months to look at
    next_click_counter = 4

    while not date_elements_list and next_click_counter != 0:
        date_elements = driver.find_elements(
            By.XPATH, "//table[@class='ui-datepicker-calendar']//a"
        )
        date_elements_list.extend(date_elements)

        driver.find_element(
            By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a'
        ).click()
        time.sleep(uniform(0.5, 1.5))

        next_click_counter -= 1

    if date_elements_list:
        # select the first date
        date_elements_list[0].click()
        logging.info(f"Found availability at: {option.text}")
    else:
        # click on a trivial element to close the datepicker
        action.move_to_element(
            driver.find_element(
                By.XPATH,
                '//*[@id="appointment-form"]/fieldset/ol/fieldset/div/div[3]/div[1]/strong',
            )
        )
        action.click().perform()

        logging.info(f"Browsed through city: {option.text}. No availability found")
        continue

    date_val = datepicker.get_attribute("value")

    # extract available time slots for the selected date
    time_select = Select(
        driver.find_element(By.ID, "appointments_consulate_appointment_time")
    )
    availability[option.text][date_val] = time_select.options[1:].text

with open(LOG_PATH, "r") as f:
    logs = f.read()

message = f"""
Script execution started at {script_exec_dt}.

Availability JSON: {json.dumps(obj=availability, indent=4, sort_keys=True)}

Logs for the script run: {logs}
"""

# send the json to telegram
send_message(message)
