# coding=utf-8
from datetime import datetime

_DATE_FORMATTER = '%d.%m.%Y'

CAMPAIGN_NAME = 'My Test Campaign 2014'
PRODUCT_TYPE = 'Мобильные сайты'
PADS_TYPE = 'Мобильные версии сервисов и приложений Mail.Ru'
BANNER_DATA = {
    'url': 'test.com',
    'image_uri': './img2.jpg'
}

INCOME_TARGETING = 'Средний'
FROM_DATE = datetime.strptime('01.01.2015', _DATE_FORMATTER)
TO_DATE = datetime.strptime('01.08.2015', _DATE_FORMATTER)