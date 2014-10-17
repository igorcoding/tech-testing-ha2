# coding=utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from tests.pages.common import *


class CreateAdPage(Page):
    PATH = '/ads/create'

    PAGE_CONTENT = (By.CLASS_NAME, 'create-page')

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def product_type(self):
        return ProductType(self.driver)

    @property
    def targeting_type(self):
        return PadType(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    def wait_for_load(self):
        self.wait_for_item_load(*self.PAGE_CONTENT)


class TopMenu(Component):
    EMAIL = (By.CSS_SELECTOR, '#PH_user-email')

    def get_email(self):
        return WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(*self.EMAIL).text
        )


class ProductType(RadioButtonComponent):
    PRODUCT_TYPES = (By.CSS_SELECTOR, ".base-setting__product-type")

    def select_product(self, product_name):
        products = self.driver.find_element(*self.PRODUCT_TYPES)
        radio_input = products.find_element(By.XPATH, self.RADIO_BUTTON_XPATH % product_name)
        radio_input.click()


class PadType(RadioButtonComponent):
    TARGETING_TYPES = (By.CSS_SELECTOR, ".base-setting__pads-targeting")

    def select_pad(self, targeting_name):
        products = self.driver.find_element(*self.TARGETING_TYPES)
        radio_input = products.find_element(By.XPATH, self.RADIO_BUTTON_XPATH % targeting_name)
        radio_input.click()


class BannerForm(Component):
    BANNER_FORM = (By.CLASS_NAME, 'banner-form')
    SAVE_BANNER_BUTTON = (By.CLASS_NAME, 'banner-form__save-button')
    ADDED_BANNERS = (By.CSS_SELECTOR, '.added-banner__banners-wrapper>li')

    URL_INPUT = (By.XPATH, ".//input[@type='text'][@data-name='url']")
    IMAGE_INPUT = (By.XPATH, ".//input[@type='file'][@data-name='image']")
    # IMAGE_INPUT = (By.CSS_SELECTOR, '.banner-form__img-file-cont')

    def __init__(self, driver):
        super(BannerForm, self).__init__(driver)
        self.banner_form = self.driver.find_element(*self.BANNER_FORM)

    def _find_visible_element(self, parent, selector):
        if parent is None:
            parent = self.driver
        elems = parent.find_elements(*selector)
        elem = None
        for e in elems:
            if e.is_displayed():
                elem = e
                break
        if elem is None:
            raise Exception("Couldn't find visible to user element")
        return elem

    def set_url(self, url):
        # url_input = self.driver.find_element(*self.URL_INPUT)
        url_input = self._find_visible_element(None, self.URL_INPUT)
        url_input.send_keys(url)

    def set_image(self, image_uri):
        img_input = self.driver.find_element(*self.IMAGE_INPUT)
        # img_input = self._find_visible_element(None, self.IMAGE_INPUT)
        img_input.send_keys(image_uri)

        def banner_waiting(driver):
            banners = driver.find_elements(By.CLASS_NAME, "banner-preview__img")
            for b in banners:
                if b.value_of_css_property("display") == 'block':
                    return b

        banner = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(banner_waiting)
        WebDriverWait(banner, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda b: (b.value_of_css_property("background-image") is not None)
        )

    def submit(self):
        self.driver.find_element(*self.SAVE_BANNER_BUTTON).click()
        added_banners = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_elements(*self.ADDED_BANNERS)
        )
        if len(added_banners) == 1:
            return added_banners[0]
        return None

    def fill_banner(self, url, image_uri):
        self.set_url(url)
        self.set_image(image_uri)
        return self.submit()

