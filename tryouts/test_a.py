# -*- coding:utf-8 -*-
import logging
import os
import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from libs.erp_pages import wait_for_element


class TestTeacherManagement(object):
    def test_teacher_management(self, teacher_management):
        driver = teacher_management
        try:
            query_teachername = wait_for_element(driver, '//*[@id="TeacherName"]')

            query_teachername.clear()
            query_teachername.send_keys(u'管理员(admin)')
            #
            query_res_teachername = wait_for_element(driver,
                                                     '//*[@id="search_par_panel_body_master"]/div/div[20]/div/div/ul/li/a')

            hover = ActionChains(driver).move_to_element(query_res_teachername)
            hover.click().perform()
            query_btn = wait_for_element(driver,
                                         '//*[@id="search_par_panel_body_master"]/div/div[24]/button[2]')

            hover = ActionChains(driver).move_to_element(query_btn)
            hover.click().perform()
            #
            scheduled_table = wait_for_element(driver,
                                               '//*[@id="data_body_info"]/table/tbody/tr/td[5]/a')

            hover = ActionChains(driver).move_to_element(scheduled_table)
            hover.click().perform()
            time.sleep(int(os.environ.get('sleep_time')))

            if driver.title != u'管理员(admin)课程表':
                logging.info('need to change to schedule table tab')
            changed_tab = False
            if len(driver.window_handles) > 1:
                #
                for window_handle in driver.window_handles:
                    driver.switch_to_window(window_handle)
                    if driver.title == u'管理员(admin)课程表':
                        logging.info('changed to schedule table tab')
                        changed_tab = True
                        break
            logging.info('title is : %s' % driver.title)

            assert changed_tab

            changed_back = False
            if len(driver.window_handles) > 1:
                #
                for window_handle in driver.window_handles:
                    driver.switch_to_window(window_handle)
                    if driver.title == u'Erp管理系统':
                        logging.info('changed back ')
                        changed_back = True
                        break
            assert changed_back

        except Exception, e:
            logging.exception(str(e))
            pytest.fail('failed !')
