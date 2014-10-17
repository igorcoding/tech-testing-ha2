import urlparse
from selenium.webdriver.support.wait import WebDriverWait

WEB_DRIVER_DEFAULT_WAIT = 30
WEB_DRIVER_POLL_FREQ = 0.1


class Component(object):
    def __init__(self, driver):
        self.driver = driver

    def wait_for_item_load(self, by, selector):
        return WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(by, selector)
        )


class Page(Component):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class RadioButtonComponent(Component):
    RADIO_BUTTON_XPATH = ".//label[text() = '%s']/../input"