# coding=utf-8
import unittest
from tests.basic_testcase import BasicTestCase
from tests.pages.campaigns import CampaignsPage
from tests.pages.create_ad import CreateAdPage, IncomeTargeting
from tests.test_data import *
from util import list_to_str


class AdEditTest(BasicTestCase):

    def setUp(self):
        super(AdEditTest, self).setUp()
        self._make_campaign()

    def tearDown(self):
        super(AdEditTest, self).tearDown()
        self._remove_campaign()

    def _make_campaign(self):
        ad_page = CreateAdPage(self.driver)
        self._fill_basic_settings(ad_page)

        ad_page.banner_form.fill_banner(**BANNER_DATA)

        income_setting = ad_page.income_targeting
        income_setting.toggle_settings()
        for income in INCOME_TARGETINGS:
            income_setting.choose(income)

        ad_page.campaign_time.toggle_settings().fill(FROM_DATE, TO_DATE)
        ad_page.submit_campaign()

    def _remove_campaign(self):
        pass

    # @unittest.SkipTest
    def test_campaign_name_correct(self):
        """
            Проверка правильности имени кампании
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        name = my_campaign_editor.base_settings.get_campaign_name()
        self.assertEqual(CAMPAIGN_NAME, name)

    # @unittest.SkipTest
    def test_pad_correct(self):
        """
            Проверка правильности площадки
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        pad = my_campaign_editor.base_settings.get_pad()
        self.assertEqual(PAD_TYPE, pad)

    # @unittest.SkipTest
    def test_banner_preview_correct(self):
        """
            Проверка правильности данных в баннере
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        banner_preview = my_campaign_editor.banner_preview
        url = banner_preview.get_url()

        self.assertIn(BANNER_DATA['url'], url, 'Seems like url is not correct')

    # @unittest.SkipTest
    def test_income_correct(self):
        """
            Проверяет то, что income был сохранен верно
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        income = my_campaign_editor.income_targeting
        text = income.get_header_text()

        income.toggle_settings()
        all_incomes_checked, not_checked = income.check_chosen(INCOME_TARGETINGS)

        self.assertEqual(text, IncomeTargeting.HEADER_SELECTED_TEXT, 'No feedback about his (her) actions')
        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % list_to_str(not_checked))

    # @unittest.SkipTest
    def test_dates_correct(self):
        """
            Проверяет то, что даты работы кампании были сохранены верно
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        campaign_time = my_campaign_editor.campaign_time
        campaign_time.toggle_settings()

        from_date, to_date = campaign_time.get_dates()

        self.assertEqual(FROM_DATE, from_date, 'From date is incorrect')
        self.assertEqual(TO_DATE, to_date, 'To date is incorrect')

    # @unittest.SkipTest
    def test_dates_delta_correct(self):
        """
            Проверяет то, что разница между днями посчитана верно
        """
        campaigns_page = CampaignsPage(self.driver)
        my_campaign_editor = campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

        campaign_time = my_campaign_editor.campaign_time
        campaign_time.toggle_settings()

        delta = int(campaign_time.get_length_in_days())
        actual_delta = (TO_DATE - FROM_DATE).days + 1

        self.assertEqual(actual_delta, delta)