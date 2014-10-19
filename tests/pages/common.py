import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

WEB_DRIVER_DEFAULT_WAIT = 30
WEB_DRIVER_POLL_FREQ = 0.1


class Component(object):
    def __init__(self, driver):
        self.driver = driver

    def wait_for_item_load(self, by, selector):
        return self.wait_for_item_load_by_parent(self.driver, by, selector)

    @staticmethod
    def wait_for_item_load_by_parent(parent, by, selector):
        return WebDriverWait(parent, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(by, selector)
        )

    def _find_visible_element(self, parent, selector):
        if parent is None:
            parent = self.driver

        elems = WebDriverWait(parent, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda p: p.find_elements(*selector)
        )
        elem = None
        for e in elems:
            if e.is_displayed():
                elem = e
                break
        if elem is None:
            raise Exception("Couldn't find visible to user element")
        return elem


class Page(Component):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class TopMenu(Component):
    EMAIL = (By.CSS_SELECTOR, '#PH_user-email')

    def get_email(self):
        return WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(*self.EMAIL).text
        )


class LabeledInputComponent(Component):
    LABELED_INPUT_XPATH = ".//label[text() = '%s']/../input"