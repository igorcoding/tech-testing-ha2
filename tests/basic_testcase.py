import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from tests.pages.auth import AuthPage
from tests.test_data import *


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self._login()

    def tearDown(self):
        self.driver.quit()

    def _login(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        logged_in = auth_page.login(USERNAME, DOMAIN, PASSWORD)
        if not logged_in:
            raise Exception("Couldn't login")

    def _fill_basic_settings(self, ad_page):
        base_settings = ad_page.campaign_base_settings
        base_settings.set_campaign_name(CAMPAIGN_NAME)
        base_settings.set_product_type(PRODUCT_TYPE)
        base_settings.set_pad_type(PAD_TYPE)