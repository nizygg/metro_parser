import json
import re

from bs4 import BeautifulSoup, PageElement

from init_data import ENCODING


def get_page_in_html(path_to_html) -> BeautifulSoup:
    """Получаем страницу BeautifulSoup в из файла .html"""
    with open(path_to_html, 'r', encoding=ENCODING) as file:
        index_html = file.read()

    return BeautifulSoup(index_html, 'lxml')


def get_brands(soup: BeautifulSoup) -> list:
    """Получаем все возможные бренды из каталога на сайте"""
    brands: list[str] = (
        (
            soup.find('div', class_='catalog-checkbox-group')
            .text.replace('\n', '').strip().lower().split('            ')
        )
    )
    brands.remove('без бренда')
    return brands


def get_int_sum_out_of_element(price: PageElement) -> float:
    """Получает целую часть сумму из элемента"""
    str_int_price = price.find(
        'span',
        class_='product-price__sum-rubles'
    ).text.replace(" ", "")

    return float(re.sub(r'\W+', '', str_int_price))


def get_penny_sum_out_of_element(price: PageElement) -> float:
    """Получает копеечную часть суммы из элемента"""
    _float = price.find('span', class_='product-price__sum-penny')
    str_float_price = (
        BeautifulSoup('0', 'lxml') if _float is None else _float
    )
    return float(re.sub(r'\W+', '', str_float_price.text))


def calculate_int_and_penny_sums(
        class_: PageElement) -> float:
    """Складывает целую и копеечную части"""
    int_price = get_int_sum_out_of_element(
        class_
    )

    float_price = get_penny_sum_out_of_element(
        class_
    )

    return int_price + float_price / 100


def get_regular_price_out_of_element(el, promo_price: float) -> float:
    """Возвращает"""
    regular_price = (
        el.find(
            'div',
            class_='catalog-2-level-product-card__offline-range-top'
        ).find('span', class_='product-price__sum-rubles')
    )
    return (
        promo_price if regular_price is None else float(
            re.sub(r'\W+', '', regular_price.text)
        )
    )


def making_list_of_items(soup: BeautifulSoup, id=1) -> dict:
    """Создаем список из html страницы"""
    elements = soup.find_all(attrs={'data-sku': True})
    products_available = {}
    for el in elements:
        artical_num = el['data-sku']
        brand = 'Без бренда'
        reference = (
            'https://online.metro-cc.ru'
            + el.find('a', attrs={'href': True})['href']
        )
        name = el.find('span', class_='product-card-name__text').text.strip()
        for _brand in get_brands(soup):
            if _brand in name.lower():
                brand = _brand
        # Все ценны из тегов конкретного продукта
        prices = el.find(
            'ul',
            class_='product-range-prices__items').find_all(
                'li', class_='product-range-prices__item'
            )

        # Если длина цен больше двух, значит есть оптовая цена,
        # иначе выводим промо цену
        if len(prices) > 1:
            regular_price = calculate_int_and_penny_sums(
                prices[0]
            )

            wholesale_price = {
                'Цена': calculate_int_and_penny_sums(prices[1]),
                'Минимальное кол-во для приобретения': int(
                    (
                        prices[1]
                        .find('span', class_='product-range-prices__item-count')
                        .text.split()
                    )[1]
                ),
            }
        else:
            promo_price = calculate_int_and_penny_sums(
                prices[0]
            )
            regular_price = (get_regular_price_out_of_element(el, promo_price))

            promo_price = (
                'Отсутствует' if regular_price == promo_price else promo_price
            )

            wholesale_price = None

        products_available[id] = {
            'Артикул': artical_num,
            'Ссылка на товар': reference,
            'Бренд': brand,
            'Наименование товара': name,
            'Постоянная цена': regular_price,
            'Оптовая цена': (
                wholesale_price if wholesale_price is not None
                else 'Отсутствует'
            ),
            'Промо цена': promo_price if len(prices) < 2 else 'Отсутствует'
        }
        id += 1

    return products_available


def parse_to_json(data, city, center):
    """Парсим данные в json"""

    with open(
        f'../json_result/{city}/data_{center}.json',
        'w',
        encoding=ENCODING
    ) as file:
        return json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4, sort_keys=True
        )
