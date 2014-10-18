# coding=utf-8
from selenium.webdriver.common.by import By
from tests.pages.common import *


class CreateAdPage(Page):
    PATH = '/ads/create'

    PAGE_CONTENT = (By.CLASS_NAME, 'create-page')
    SUBMIT_CAMPAIGN_BUTTON = (By.CLASS_NAME, 'main-button__label')

    @property
    def campaign_base_settings(self):
        return CampaignBaseSettings(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    @property
    def income_targeting(self):
        return IncomeTargeting(self.driver)

    @property
    def campaign_time(self):
        return CampaignTimeTargeting(self.driver)

    def submit_campaign(self):
        self.driver.find_element(*self.SUBMIT_CAMPAIGN_BUTTON).click()

    def wait_for_load(self):
        self.wait_for_item_load(*self.PAGE_CONTENT)


class CampaignBaseSettings(Component):
    CAMPAIGN_NAME_INPUT = (By.CLASS_NAME, 'base-setting__campaign-name__input')

    @property
    def product_type(self):
        return ProductType(self.driver)

    @property
    def pad_type(self):
        return PadType(self.driver)

    def set_campaign_name(self, campaign_name):
        campaign_input = self.driver.find_element(*self.CAMPAIGN_NAME_INPUT)
        campaign_input.clear()
        campaign_input.send_keys(campaign_name)

    def set_product_type(self, product_name):
        self.product_type.select_product(product_name)

    def set_pad_type(self, pad_name):
        self.pad_type.select_pad(pad_name)


class ProductType(LabeledInputComponent):
    PRODUCT_TYPES = (By.CSS_SELECTOR, ".base-setting__product-type")

    def select_product(self, product_name):
        products = self.driver.find_element(*self.PRODUCT_TYPES)
        radio_input = products.find_element(By.XPATH, self.LABELED_INPUT_XPATH % product_name)
        radio_input.click()


class PadType(LabeledInputComponent):
    TARGETING_TYPES = (By.CSS_SELECTOR, ".base-setting__pads-targeting")

    def select_pad(self, pad_name):
        products = self.driver.find_element(*self.TARGETING_TYPES)
        radio_input = products.find_element(By.XPATH, self.LABELED_INPUT_XPATH % pad_name)
        radio_input.click()


class BannerForm(Component):
    BANNER_FORM = (By.CLASS_NAME, 'banner-form')
    SAVE_BANNER_BUTTON = (By.CLASS_NAME, 'banner-form__save-button')
    ADDED_BANNERS = (By.CSS_SELECTOR, '.added-banner__banners-wrapper>li')

    URL_INPUT = (By.XPATH, ".//input[@type='text'][@data-name='url']")
    IMAGE_INPUT = (By.XPATH, ".//input[@type='file'][@data-name='image']")

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


class TargetingComponent(Component):
    SETTING_HEADER_TEMPLATE = "//span[@class='campaign-setting__name'][text() = '%s']"
    TARGETING_NAME = ''

    def __init__(self, driver):
        super(TargetingComponent, self).__init__(driver)
        if self.TARGETING_NAME == '':
            raise Exception('TARGETING_NAME not set')

    def _get_settng_header_selector(self):
        return By.XPATH, self.SETTING_HEADER_TEMPLATE % self.TARGETING_NAME

    def unfold_settings(self):
        header = self.driver.find_element(*self._get_settng_header_selector())
        value_wrapper = header.find_element(By.XPATH, './../..')\
                              .find_element(By.CLASS_NAME, 'campaign-setting__wrapper')
        value = value_wrapper.find_element(By.CLASS_NAME, 'campaign-setting__value')
        value.click()  # unfold the targeting list

        return value_wrapper


class IncomeTargeting(TargetingComponent):
    TARGETING_NAME = 'Уровень дохода'

    def choose(self, income):
        value_wrapper = self.unfold_settings()
        content = value_wrapper.find_element(By.CSS_SELECTOR, '.campaign-setting__content .campaign-setting__detail')

        checkbox_input = content.find_element(By.XPATH, LabeledInputComponent.LABELED_INPUT_XPATH % income)
        checkbox_input.click()


class CampaignTimeTargeting(TargetingComponent):
    TARGETING_NAME = 'Время работы кампании'

    FROM_DATE = (By.CSS_SELECTOR, ".campaign-setting__detail__date-input[data-name=from]")
    TO_DATE = (By.CSS_SELECTOR, ".campaign-setting__detail__date-input[data-name=to]")
    DATE_FORMATTER = '%d.%m.%Y'

    def fill(self, from_date, to_date):

        """

        :param from_date:
         :type from_date: datetime.datetime
        :param to_date:
         :type to_date: datetime.datetime
        """

        self.unfold_settings()

        from_date = from_date.strftime(self.DATE_FORMATTER)
        to_date = to_date.strftime(self.DATE_FORMATTER)

        self.driver.find_element(*self.FROM_DATE).send_keys(from_date)
        self.driver.find_element(*self.TO_DATE).send_keys(to_date)

#


