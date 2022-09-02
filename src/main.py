import json
import time
from random import uniform

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils import log_in, send_message

url = "https://ais.usvisa-info.com/en-ca/niv/schedule/43160383/appointment"

driver = webdriver.Chrome()
driver.get(url)

# logging in
log_in(driver)

action = ActionChains(driver)

#
availability = {}

location_select = Select(
    driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
)
location_options = location_select.options[1:]
for option in location_options:
    option.click()
    availability[option.text] = {}
    time.sleep(uniform(2, 4))

    datepicker = driver.find_element(By.ID, "appointments_consulate_appointment_date")
    try:
        datepicker.click()
    except ElementNotInteractableException:
        print(f"No availability in city: {option.text}")
        continue
    time.sleep(uniform(2, 4))

    a_elements_list = []
    next_click_counter = 15

    while not a_elements_list and next_click_counter != 0:
        next_btn = driver.find_element(
            By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a'
        )
        next_btn.click()
        time.sleep(uniform(0.5, 1.5))

        a_elements = driver.find_elements(
            By.XPATH, "//table[@class='ui-datepicker-calendar']//a"
        )
        a_elements_list.extend(a_elements)

        next_click_counter -= 1

    if a_elements_list:
        a_elements_list[0].click()
    else:
        action.move_to_element(
            driver.find_element(
                By.XPATH, '//*[@id="appointment-form"]/fieldset/ol/fieldset/legend'
            )
        )
        action.click()
        action.perform()

        continue

    date_val = datepicker.get_attribute("value")

    time_select = Select(
        driver.find_element(By.ID, "appointments_consulate_appointment_time")
    )
    availability[option.text][date_val] = time_select.options[1:].text

send_message(json.dumps(availability))
