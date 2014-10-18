from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from common import Page, Component
from tests.pages.create_ad import CreateAdPage


class AuthPage(Page):
    PATH = '/login'

    @property
    def _form(self):
        return AuthForm(self.driver)

    def fill_form(self, login, domain, pwd):
        form = self._form
        form.set_login(login)
        form.set_domain(domain)
        form.set_password(pwd)

        form.submit()

    def login(self, login, domain, pwd):
        """

        :param login:
        :param domain:
        :param pwd:
        :return:
        """
        self.fill_form(login, domain, pwd)

        create_page = CreateAdPage(self.driver)
        create_page.open()

        email = create_page.top_menu.get_email()
        return email == login


class AuthForm(Component):
    LOGIN = (By.ID, 'id_Login')
    PASSWORD = (By.ID, 'id_Password')
    DOMAIN = (By.ID, 'id_Domain')
    SUBMIT = (By.CSS_SELECTOR, '#gogogo>input')

    def set_login(self, login):
        self.driver.find_element(*self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element(*self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element(*self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element(*self.SUBMIT).click()