# coding=utf-8
from datetime import datetime
import os

_DATE_FORMATTER = '%d.%m.%Y'

DOMAIN = '@bk.ru'
USERNAME = 'tech-testing-ha2-16' + DOMAIN
PASSWORD = os.environ['TTHA2PASSWORD']

CAMPAIGN_NAME = 'My Test Campaign 2014'
PRODUCT_TYPE = 'Мобильные сайты'
PADS_TYPE = 'Мобильные версии сервисов и приложений Mail.Ru'
BANNER_DATA = {
    'url': 'test.com',
    'image_uri': './res/img2.jpg'
}

INCOME_TARGETINGS = {
    'Средний'
}
FROM_DATE = datetime.strptime('01.01.2015', _DATE_FORMATTER)
TO_DATE = datetime.strptime('01.08.2015', _DATE_FORMATTER)