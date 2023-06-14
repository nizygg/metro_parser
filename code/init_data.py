import logging

ENCODING = 'utf-8'

CITIES = {
    'moscow': (
        '//*[@id="__layout"]/div/div/div[7]/div/'
        'div/section/div/div[2]/div/span[1]'
    ),
    'saint_petersburg': (
        '//*[@id="__layout"]/div/div/div[7]/div/'
        'div/section/div/div[2]/div/span[2]'
    ),
}

ALL_CENTERS = {
    'moscow': {
        'Leningradskaya_71': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select'
            ' > div:nth-child(2) > div > div.multiselect__content-wrapper'
            ' > ul > li:nth-child(1) > span > span'
        ),
        # 'ProspectMira_211': None,
        # 'Doroznaya_1': None,
        # 'Ryabinova_59': None,
        # 'Dmitrovskoe_165B': None,
        # 'Proshlakova_14': None,
        'MKAD_104': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select >'
            ' div:nth-child(2) > div > div.multiselect__content-wrapper'
            ' > ul > li:nth-child(7) > span > span'
        ),
        # 'Shosseinaya_2B': None,
        # 'Moskovskiy_34': None,
        # 'Skladochnaya_1': None,
        # 'Dubrovskaya_13A': None,
        'Borovskoe_10A': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select >'
            ' div:nth-child(2) > div > div.multiselect__content-wrapper >'
            ' ul > li:nth-child(12) > span > span'
        ),
    },
    'saint_petersburg': {
        'Comendantskiy_3': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select'
            ' > div:nth-child(2) > div > div.multiselect__content-wrapper'
            ' > ul > li:nth-child(1) > span > span'
        ),
        'Kosygina_4': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select'
            ' > div:nth-child(2) > div > div.multiselect__content-wrapper'
            ' > ul > li:nth-child(2) > span'
        ),
        'Pulkovskoe_23': (
            'body > div.dialog-root > div > div > div > div.receipt-order'
            ' > div:nth-child(1) > div.pickup > div.pickup__select'
            ' > div:nth-child(2) > div > div.multiselect__content-wrapper'
            ' > ul > li:nth-child(3) > span'
        ),
    }
}

TIME_DELAY = 3

file_handler = logging.FileHandler(
    filename='../logs/main.log',
    mode='w',
    encoding=ENCODING,
)
logger = logging.getLogger(__name__)
file_handler.setFormatter(
    logging.Formatter('%(levelname)s - %(module)s - %(message)s'))
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
