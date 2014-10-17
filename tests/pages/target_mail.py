from common import Page
from tests.pages.auth import AuthPage


class TargetMail(Page):

    def login(self, login, domain, pwd):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        return auth_page.login(login, domain, pwd)
