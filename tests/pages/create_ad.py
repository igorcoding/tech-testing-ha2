# coding=utf-8
from datetime import datetime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions

from tests.pages.common import *


class CreateAdPage(Page):
    PATH = '/ads/create'

    PAGE_CONTENT = (By.CLASS_NAME, 'create-page')
    SUBMIT_CAMPAIGN_BUTTON = (By.CLASS_NAME, 'main-button__label')

    def open(self):
        super(CreateAdPage, self).open()
        self.wait_for_load()

    @property
    def campaign_base_settings(self):
        return CampaignBaseSettings(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    @property
    def banner_preview(self):
        return BannerPreview(self.driver)

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


class BannerComponent(Component):
    URL_INPUT = (By.XPATH, ".//input[@type='text'][@data-name='url']")
    IMAGE_INPUT = (By.XPATH, ".//input[@type='file'][@data-name='image']")


class BannerForm(BannerComponent):
    SAVE_BANNER_BUTTON = (By.CLASS_NAME, 'banner-form__save-button')

    def __init__(self, driver):
        super(BannerForm, self).__init__(driver)

    def set_url(self, url):
        url_input = self._find_visible_element(None, self.URL_INPUT)
        url_input.send_keys(url)

    def set_image(self, image_uri):
        img_input = self.driver.find_element(*self.IMAGE_INPUT)
        img_input.send_keys(image_uri)

        BannerPreview.wait_for_preview(self.driver)

    def submit(self):
        self.driver.find_element(*self.SAVE_BANNER_BUTTON).click()
        return BannerPreview(self.driver)

    def fill_banner(self, url, image_uri):
        """
        :return: Banner preview that is in added_banners section on page
        :rtype: BannerPreview
        """
        self.set_url(url)
        self.set_image(image_uri)
        return self.submit()


class BannerPreview(BannerComponent):
    ADDED_BANNERS = (By.CSS_SELECTOR, '.added-banner__banners-wrapper>li')
    BANNER_FORM = (By.CSS_SELECTOR, '.banner-form.free-block')
    BANNER_PREVIEW_IMG = (By.CLASS_NAME, "banner-preview__img")
    PREVIEW_EDIT_BUTTON = (By.CSS_SELECTOR, '.added-banner__buttons-panel .added-banner__button_edit')

    def __init__(self, driver):
        super(BannerPreview, self).__init__(driver)
        banners = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_elements(*self.ADDED_BANNERS)
        )
        if len(banners) == 1:
            self.banner = banners[0]
        else:
            raise Exception('Count of banners is %d instead of 1 somehow' % len(banners))

    def get_url(self):
        self.wait_for_preview(self.driver)

        edit_button = self.wait_for_item_load_by_parent(self.banner, *self.PREVIEW_EDIT_BUTTON)
        builder = ActionChains(self.driver)
        builder.move_to_element(self.banner).click(edit_button).perform()

        # Waiting for banner preview form to popup
        banner_form = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda b: b.find_element(*self.BANNER_FORM)
        )

        url_input = banner_form.find_element(By.CSS_SELECTOR, '.banner-form__row[data-name=url][style="display: list-item;"] input[type=text]')
        # url_input = self._find_visible_element(banner_form, self.URL_INPUT)
        return url_input.get_attribute('value')

    @staticmethod
    def wait_for_preview( driver):
        def banner_waiting(d):
            banners = d.find_elements(*BannerPreview.BANNER_PREVIEW_IMG)
            for b in banners:
                if b.value_of_css_property("display") == 'block':
                    return b

        banner = WebDriverWait(driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(banner_waiting)
        WebDriverWait(banner, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda b: (b.value_of_css_property("background-image") is not None)
        )


class TargetingComponent(Component):
    SETTING_HEADER_TEMPLATE = "//span[@class='campaign-setting__name'][text() = '%s']"
    TARGETING_NAME = ''

    def __init__(self, driver):
        super(TargetingComponent, self).__init__(driver)
        if self.TARGETING_NAME == '':
            raise Exception('TARGETING_NAME not set')

        self.settings_visible = False

    def _get_settng_header_selector(self):
        return By.XPATH, self.SETTING_HEADER_TEMPLATE % self.TARGETING_NAME

    def toggle_settings(self):
        value, value_wrapper = self._get_value_and_wrapper()

        value.click()  # toggle the targeting list
        self.settings_visible = not self.settings_visible
        return self

    def _get_value_and_wrapper(self):
        header = self.wait_for_item_load(*self._get_settng_header_selector())
        value_wrapper = header.find_element(By.XPATH, './../..') \
            .find_element(By.CLASS_NAME, 'campaign-setting__wrapper')

        value = WebDriverWait(value_wrapper, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(By.CLASS_NAME, 'campaign-setting__value')
        )

        return value, value_wrapper


class IncomeTargeting(TargetingComponent):
    TARGETING_NAME = u'Уровень дохода'
    HEADER_SELECTED_TEXT = u'Выбран'

    CHECKBOXES = (By.NAME, 'input')

    def _get_content(self):
        _, value_wrapper = self._get_value_and_wrapper()
        content = value_wrapper.find_element(By.CSS_SELECTOR, '.campaign-setting__content .campaign-setting__detail')
        return content

    def choose(self, income):
        content = self._get_content()

        checkbox_input = content.find_element(By.XPATH, LabeledInputComponent.LABELED_INPUT_XPATH % income)
        checkbox_input.click()

    def check_chosen(self, incomes):
        content = self._get_content()

        not_chosen = []
        for income in incomes:
            checkbox_input = content.find_element(By.XPATH, LabeledInputComponent.LABELED_INPUT_XPATH % income)
            if not checkbox_input.is_selected():
                not_chosen.append(income)

        all_chosen = len(not_chosen) == 0
        return all_chosen, not_chosen

    def get_header_text(self):
        _, value_wrapper = self._get_value_and_wrapper()
        return value_wrapper.find_element(By.CLASS_NAME, 'campaign-setting__value').text


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

        from_date = from_date.strftime(self.DATE_FORMATTER)
        to_date = to_date.strftime(self.DATE_FORMATTER)

        self.driver.find_element(*self.FROM_DATE).send_keys(from_date)
        self.driver.find_element(*self.TO_DATE).send_keys(to_date)

    def get_length_in_days(self):
        _, value_wrapper = self._get_value_and_wrapper()

        days_text_elem = self.wait_for_item_load_by_parent(value_wrapper, By.CLASS_NAME, 'campaign-setting__value')
        days_text = days_text_elem.text.split()[0]  # getting only a number
        return days_text

    def get_dates(self):
        """

        :rtype: (datetime.datetime, datetime.datetime)
        """

        self.toggle_settings()
        from_date = self.driver.find_element(*self.FROM_DATE).get_attribute('value')
        to_date = self.driver.find_element(*self.TO_DATE).get_attribute('value')

        return datetime.strptime(from_date, self.DATE_FORMATTER), datetime.strptime(to_date, self.DATE_FORMATTER)



