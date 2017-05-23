import ConfigParser
import logging
import os
import sys
import time

import pytest
from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

sleep_time = 2
# os.environ['sleep_time'] = 0

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

local_path = os.path.abspath(os.path.dirname(__file__))

local_conf_path = os.path.join(os.path.dirname(local_path), 'local.conf')

if not os.path.exists(local_conf_path):
    raise Exception('no local.conf found , ATUI/local.conf is need !')
else:
    logging.debug('using %s as local conf' % local_conf_path)

cf = ConfigParser.ConfigParser()
#
cf.read(local_conf_path)
#
#
os.environ.update(dict(cf.items("urls")))
os.environ.update(dict(cf.items("drivers")))
os.environ.update(dict(cf.items("user_info")))

loc_atui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if loc_atui not in sys.path:
    sys.path.append(loc_atui)

from libs.erp_pages import wait_for_element_tobe_interactable


# ******************************************************************************************************************
@pytest.fixture(scope='class')
def web_browser_firefox(request):
    firefox_browser = webdriver.Firefox()

    def fin():
        firefox_browser.quit()

    request.addfinalizer(fin)
    return firefox_browser


@pytest.fixture(scope='class')
def login(request, web_browser_firefox):
    driver = web_browser_firefox
    try:

        driver.get(os.environ.get('erp_url'))
        driver.maximize_window()

        usrname_input = wait_for_element_tobe_interactable(driver, '//*[@id="mainLogin"]/form/div[1]/div/input')
        usrname_input.clear()
        usrname_input.send_keys(os.environ.get('username'))

        #
        passwd_input = wait_for_element_tobe_interactable(driver, '//*[@id="mainLogin"]/form/div[2]/div/input')

        passwd_input.clear()
        passwd_input.send_keys(os.environ.get('password'))

        #
        login_btn = wait_for_element_tobe_interactable(driver, '//*[@id="mainLogin"]/form/div[5]/button')

        login_btn.click()

        time.sleep(sleep_time)
    except Exception, e:
        logging.exception(str(e))

    def fin():
        usr_topright_span = wait_for_element_tobe_interactable(driver,
                                                               '//*[@id="layout_menu_header"]/div/ul[3]/li[4]/a')

        usr_topright_span.click()
        quit_span = wait_for_element_tobe_interactable(driver,
                                                       '//*[@id="layout_menu_header"]/div/ul[3]/li[4]/ul/li[2]/a')

        # quit_span.click()
        hover = ActionChains(driver).move_to_element(quit_span)
        hover.click().perform()
        time.sleep(sleep_time)

    request.addfinalizer(fin)


@pytest.fixture()
def teacher_management(request, login, web_browser_firefox):
    driver = web_browser_firefox

    try:
        #
        span_education_dpt = wait_for_element_tobe_interactable(driver,
                                                                '//*[@id="autobay_layout_sidebar"]/div/div/div/ul/li[3]/a/i[2]')

        hover = ActionChains(driver).move_to_element(span_education_dpt)

        teacher_mgmt = wait_for_element_tobe_interactable(driver,
                                                          '//*[@id="autobay_layout_sidebar"]/div/div/div/ul/li[3]/ul/li[1]/a/span')

        hover = hover.move_to_element(teacher_mgmt)
        hover.click().perform()

        time.sleep(sleep_time)
    except Exception, e:
        logging.exception(str(e))

    return driver
