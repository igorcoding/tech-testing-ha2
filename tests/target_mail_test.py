# coding=utf-8
import os

import unittest

from selenium.webdriver import ActionChains, DesiredCapabilities, Remote


# class Slider(Component):
#     SLIDER = (By.CSS_SELECTOR, '.price-slider__begunok')
#
#     def move(self, offset):
#         element = WebDriverWait(self.driver, 30, 0.1).until(
#             lambda d: d.find_element(*self.SLIDER)
#         )
#         ac = ActionChains(self.driver)
#         ac.click_and_hold(element).move_by_offset(offset, 0).perform()
from tests.pages.target_mail import TargetMail
from tests.test_data import *


class TargetMailRuTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.domain = '@bk.ru'
        self.username = 'tech-testing-ha2-16' + self.domain
        self.password = os.environ['TTHA2PASSWORD']
        self.target_main = TargetMail(self.driver)

    def tearDown(self):
        self.driver.quit()

    # def test_auth(self):
    #     create_ad_page = self.target_main.login(self.username, self.domain, self.password)
    #     self.assertIsNotNone(create_ad_page, "Could not login into target.main.ru")

    def test_BETA(self):
        ad_page = self.target_main.login(self.username, self.domain, self.password)
        ad_page.wait_for_load()

        ad_page.product_type.select_product(PRODUCT_TYPE)
        ad_page.targeting_type.select_pad(PADS_TYPE)
        ad_page.banner_form.fill_banner(**BANNER_DATA)


        import time
        time.sleep(4)





        # ## And some examples
        # create_page.slider.move(100)
        # FILE_PATH = '/Users/bayandin/repos/tech-testing-selenium-demo/img.jpg'
        # element = WebDriverWait(self.driver, 30, 0.1).until(
        #     lambda d: d.find_element_by_css_selector('.banner-form__img-file')
        # )
        #
        # element.send_keys(FILE_PATH)