import time
from selenium import webdriver

# import w
# import selenium.
caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
caps['ignoreProtectedModeSettings'] = True
# caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS']=True
# driver = webdriver.Ie(capabilities=caps)
driver = webdriver.Firefox()
# self.driver.maximize_window()
# Optional argument, if not specified will search path.

driver.get('http://www.baidu.com/')
time.sleep(5)  # Let the user actually see something!
search_box = driver.find_element_by_id('kw')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
