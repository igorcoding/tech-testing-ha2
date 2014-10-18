# coding=utf-8
import unittest
from tests.basic_testcase import BasicTestCase

from tests.pages.campaigns import CampaignsPage
from tests.pages.create_ad import CreateAdPage
from tests.test_data import *
from util import list_to_str


class AdCreationTest(BasicTestCase):

    def setUp(self):
        super(AdCreationTest, self).setUp()

    def tearDown(self):
        super(AdCreationTest, self).tearDown()

    @unittest.SkipTest
    def test_banner_preview(self):
        """
            Проверяет правильность данных в засабмиченном баннере
        """
        ad_page = CreateAdPage(self.driver)
        self._fill_basic_settings(ad_page)
        ad_page.banner_form.fill_banner(**BANNER_DATA)

        banner_preview = ad_page.banner_preview
        url = banner_preview.get_url()

        self.assertEqual(BANNER_DATA['url'], url, "Entered url doesn't match the one in banner_preview")

    @unittest.SkipTest
    def test_incomes_on_toggling(self):
        """
            Проверка того, что данные в income сохраняются при сворачивании списка настроек
        """
        ad_page = CreateAdPage(self.driver)
        self._fill_basic_settings(ad_page)
        ad_page.banner_form.fill_banner(**BANNER_DATA)

        income_setting = ad_page.income_targeting
        income_setting.toggle_settings()  # opening
        for income in INCOME_TARGETINGS:
            income_setting.choose(income)

        income_setting.toggle_settings()  # closing
        all_incomes_checked, not_checked = income_setting.check_chosen(INCOME_TARGETINGS)

        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % list_to_str(not_checked))

    @unittest.SkipTest
    def test_BETA(self):
        ad_page = CreateAdPage(self.driver)
        self._fill_basic_settings(ad_page)

        ad_page.banner_form.fill_banner(**BANNER_DATA)

        income_setting = ad_page.income_targeting
        income_setting.toggle_settings()
        for income in INCOME_TARGETINGS:
            income_setting.choose(income)

        ad_page.campaign_time.toggle_settings().fill(FROM_DATE, TO_DATE)
        ad_page.submit_campaign()

        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        income = my_campaign_editor.income_targeting
        income.toggle_settings()
        all_incomes_checked, not_checked = income.check_chosen(INCOME_TARGETINGS)
        text = income.get_header_text()

        campaign_time = my_campaign_editor.campaign_time
        campaign_time.toggle_settings()
        days = campaign_time.get_length_in_days()
        from_date, to_date = campaign_time.get_dates()


        import time
        time.sleep(4)

        pass

