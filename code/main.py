from create_html_page import ALL_CENTERS, CITIES, get_source_html
from parse_data import get_page_in_html, making_list_of_items, parse_to_json


def main():
    url = (
        'https://online.metro-cc.ru/category/'
        'chaj-kofe-kakao/chay/cherniy-chay'
    )

    for city in CITIES:
        for center in ALL_CENTERS[city]:
            get_source_html(
                url,
                center,
                city,
            )

            soup = get_page_in_html(
                f'../html_pages/{city}/index_{center}.html'
            )
            parse_to_json(making_list_of_items(soup), city, center)


if __name__ == '__main__':
    main()
