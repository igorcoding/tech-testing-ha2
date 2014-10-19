from selenium.webdriver.common.by import By
import create_ad
from tests.pages.common import Component


class EditAdPage(create_ad.CreateAdPage):
    PATH = 'ads/campaigns/%s/edit/'

    def __init__(self, driver, campaign_id):
        super(EditAdPage, self).__init__(driver)
        self.PATH = self.PATH % campaign_id

    @property
    def base_settings(self):
        return EditAdBaseSettings(self.driver)


class EditAdBaseSettings(Component):
    CAMPAIGN_NAME_INPUT = (By.CLASS_NAME, 'base-setting__campaign-name__input')
    PAD_VALUE = (By.CSS_SELECTOR, 'label.base-setting__pads-item__label')

    def get_campaign_name(self):
        campaign_input = self.driver.find_element(*self.CAMPAIGN_NAME_INPUT)
        return campaign_input.get_attribute('value')

    def get_pad(self):
        pad_label = self.driver.find_element(*self.PAD_VALUE)
        return pad_label.text