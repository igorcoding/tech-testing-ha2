from tests.pages.common import *
from tests.pages.edit_ad import EditAdPage


class CampaignsPage(Page):
    PATH = '/ads/campaigns'

    @property
    def campaigns_list(self):
        return CampaignsList(self.driver)


class CampaignsList(Component):
    CAMPAIGN_XPATH_TEMPLATE = ".//span[@class='campaign-title__name'][text()='%s']/ancestor::li[@class='campaign-row']"

    def get_campaign(self, campaign_name):
        campaign = self.wait_for_item_load(By.XPATH, self.CAMPAIGN_XPATH_TEMPLATE % campaign_name)
        return Campaign(self.driver, campaign, campaign_name)


class Campaign(Component):
    CAMPAIGN_ID = (By.CLASS_NAME, 'campaign-title__id')
    CAMPAIGN_DELETE = (By.CSS_SELECTOR, 'span.control__preset_delete')

    def __init__(self, driver, campaign, campaign_name):
        super(Campaign, self).__init__(driver)
        self.campaign = campaign

        self.campaign_name = campaign_name
        self._campaign_id = None

    @property
    def campaign_id(self):
        if self._campaign_id is None:
            self._campaign_id = self.campaign.find_element(*self.CAMPAIGN_ID).text[:-1]  # removing extra comma
        return self._campaign_id

    def edit(self):
        """
        :return: Campaign Edit page
        :rtype: tests.pages.edit_ad.EditAdPage
        """
        edit_page = EditAdPage(self.driver, self.campaign_id)
        edit_page.open()
        edit_page.wait_for_load()
        return edit_page

    def delete(self):
        delete_button = self.campaign.find_element(*self.CAMPAIGN_DELETE)
        delete_button.click()