import create_ad


class EditAdPage(create_ad.CreateAdPage):
    PATH = 'ads/campaigns/%s/edit/'

    def __init__(self, driver, campaign_id):
        super(EditAdPage, self).__init__(driver)
        self.PATH = self.PATH % campaign_id
