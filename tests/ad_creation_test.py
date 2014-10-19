# coding=utf-8
import unittest
from tests.basic_testcase import BasicTestCase

from tests.pages.campaigns import CampaignsPage
from tests.pages.create_ad import CreateAdPage, IncomeTargeting
from tests.test_data import *
from util import list_to_str


class AdCreationTest(BasicTestCase):

    def setUp(self):
        super(AdCreationTest, self).setUp()
        self.ad_page = self._create_page()

    def tearDown(self):
        super(AdCreationTest, self).tearDown()

    def _create_page(self):
        ad_page = CreateAdPage(self.driver)
        self._fill_basic_settings(ad_page)
        ad_page.banner_form.fill_banner(**BANNER_DATA)
        return ad_page

    # @unittest.SkipTest
    def test_banner_preview(self):
        """
            Проверяет правильность данных в засабмиченном баннере
        """
        banner_preview = self.ad_page.banner_preview
        url = banner_preview.get_url()

        self.assertEqual(BANNER_DATA['url'], url, "Entered url doesn't match the one in banner_preview")

    # @unittest.SkipTest
    def test_incomes_on_toggling(self):
        """
            Проверка того, что данные в income сохраняются при сворачивании списка настроек
        """
        income_setting = self.ad_page.income_targeting
        income_setting.toggle_settings()  # opening
        for income in INCOME_TARGETINGS:
            income_setting.choose(income)

        income_setting.toggle_settings()  # closing
        all_incomes_checked, not_checked = income_setting.check_chosen(INCOME_TARGETINGS)
        text = income_setting.get_header_text()
        self.assertEqual(text, IncomeTargeting.HEADER_SELECTED_TEXT, 'No feedback about his (her) actions')

        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % list_to_str(not_checked))

    # @unittest.SkipTest
    def test_dates_on_toggling(self):
        """
            Проверка того, что данные в Датах работы кампании сохраняются при сворачивании списка настроек
        """
        campaign_time = self.ad_page.campaign_time
        campaign_time.toggle_settings()  # opening
        campaign_time.fill(FROM_DATE, TO_DATE)

        campaign_time.toggle_settings()  # closing
        from_date, to_date = campaign_time.get_dates()

        self.assertEqual(FROM_DATE, from_date, 'From date is incorrect')
        self.assertEqual(TO_DATE, to_date, 'To date is incorrect')

    # @unittest.SkipTest
    def test_dates_delta_correct_toggling(self):
        """
            Проверка того, что дельта между датами выставляется верная
        """
        campaign_time = self.ad_page.campaign_time
        campaign_time.toggle_settings().fill(FROM_DATE, TO_DATE)
        campaign_time.toggle_settings()  # close dropdown

        delta = campaign_time.get_length_in_days()
        actual_delta = (TO_DATE - FROM_DATE).days + 1

        self.assertEqual(actual_delta, int(delta))

    # @unittest.SkipTest
    def test_dates_flip(self):
        """
            Проверяет обмен дат местами, в случае, если to_date < from_date
        """
        campaign_time = self.ad_page.campaign_time
        campaign_time.toggle_settings().fill(TO_DATE, FROM_DATE)  # reversed direction

        from_date, to_date = campaign_time.get_dates()

        self.assertEqual(FROM_DATE, from_date, 'From date is incorrect')
        self.assertEqual(TO_DATE, to_date, 'To date is incorrect')
