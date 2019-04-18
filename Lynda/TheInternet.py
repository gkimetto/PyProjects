"""
This is a practice script using the "http://the-internet.herokuapp.com/"
link for practice.

"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
driver = webdriver.Chrome()
driver.get("http://the-internet.herokuapp.com/")

"""
This is sample code for a dropdown 
    Example : Dropdown Example
"""

select = driver.find_element_by_link_text("Dropdown").click()
select_drpdn = Select(driver.find_element_by_id('dropdown'))
select_drpdn.select_by_index(1)
time.sleep(5)
select_drpdn.select_by_index(2)
time.sleep(5)
print "Selecting Option 1"
select_drpdn.select_by_visible_text("Option 1")
print "Selecting by value"
