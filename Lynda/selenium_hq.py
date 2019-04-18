from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://www.seleniumhq.org/")
elem_by_id = driver.find_element_by_id("q")
print "Found the element by ID:  {} [ PASSED ]".format(elem_by_id)
elem_by_name = driver.find_element_by_name("q")
print "Locate element by name : {}".format(elem_by_name)
elem_h_what_is =driver.find_element_by_xpath('//h2[@div="mainContent"]')
print "Locate the element with the heading'What is Selenium'. (Xpath), Print it"
print elem_h_what_is
print "Find the element by class 'selenium-sponsors' and print it. "
elem_by_class = driver.find_element_by_class_name('selenium-sponsors')
print "The class element 'selenium_sponsors' is {} ".format(elem_by_class)
