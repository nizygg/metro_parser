import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

from init_data import ALL_CENTERS, CITIES, ENCODING, TIME_DELAY, logger


def get_num_of_pages(driver) -> int:
    """Получаем кол-во страниц с товарами"""
    try:
        catalog_paginate = driver.find_element(
            By.XPATH,
            '//*[@id="catalog-wrapper"]/main/div[2]/nav/ul'
        ).get_attribute('outerHTML')
        soup = BeautifulSoup(catalog_paginate, 'lxml')
    except Exception:
        logger.error('возникла ошибка в get_num_of_pages()', exc_info=True)

    return int(soup.find_all('li')[-2].text)


def open_all_pages(driver, num_of_pages, city, center):
    """Пролистываем все страницы и получаем полный html код"""
    # 1 - здесь для выполнения условия i == num_of_pages,
    # которое прекращается на последней странице
    try:
        for i in range(1, num_of_pages + 1):
            if i == num_of_pages:
                with open(
                    f'../html_pages/{city}/index_{center}.html',
                    'w',
                    encoding=ENCODING
                ) as file:
                    file.write(driver.page_source)
                logger.debug(
                    'успешное выполнение, результат записан в файл'
                    f' index/{city}/{center}.html\''
                )
                break

            # Находим кнопку "Показать еще"
            find_more_button = driver.find_element(
                By.XPATH,
                '//*[@id="catalog-wrapper"]/main/div[2]/button'
            )

            # Нажимаем на кнопку "Показать еще"
            driver.execute_script(
                "arguments[0].click();", find_more_button)

            time.sleep(TIME_DELAY)
    except Exception:
        logger.error('возникла ошибка в open_all_pages()', exc_info=True)


def get_city(driver, city_xpath):
    """Получить город на странице"""
    try:
        change_city = driver.find_element(
            By.XPATH,
            (
                '//*[@id="__layout"]/div/div/div[7]/div/div/'
                'section/div/div[2]/button[2]'
            )
        )
        change_city.click()
        time.sleep(TIME_DELAY)
        choose_city = driver.find_element(By.XPATH, city_xpath)
        choose_city.click()
        time.sleep(TIME_DELAY)
        show_catalog = driver.find_element(
            By.XPATH,
            (
                '//*[@id="__layout"]/div/div/div[7]/div/'
                'div/section/div/div[1]/button/span'
            )
        )
        show_catalog.click()
        time.sleep(TIME_DELAY)
    except Exception:
        logger.error('возникла ошибка в get_city()', exc_info=True)


def get_center(driver, center_xpath):
    """Переходим к городу из center_xpath"""
    try:
        show_centers = driver.find_element(
            By.XPATH,
            (
                '//*[@id="__layout"]/div/div/div[7]/'
                'div/div/section/div/div[4]/button[2]'
            )
        )
        show_centers.click()
        time.sleep(TIME_DELAY)
        open_centers = driver.find_element(
            By.CSS_SELECTOR,
            (
                'body > div.dialog-root > div > div > div > div.receipt-order'
                ' > div:nth-child(1) > div.pickup > div.pickup__select >'
                ' div:nth-child(2) > div > div.multiselect__tags > span'
            )
        )
        open_centers.click()
        time.sleep(TIME_DELAY)
        print(center_xpath)
        choose_center = driver.find_element(By.CSS_SELECTOR, center_xpath)
        choose_center.click()
        time.sleep(TIME_DELAY)
        save_choose = driver.find_element(
            By.CSS_SELECTOR,
            (
                'body > div.dialog-root > div > div > div > div.receipt-order'
                ' > div:nth-child(1) > div.pickup > div.pickup__select'
                ' > div.pickup__apply-btn-desk > button > span'
            )
        )
        save_choose.click()
        time.sleep(TIME_DELAY)
        availability_check = driver.find_element(
            By.CSS_SELECTOR,
            (
                '#catalog-wrapper > aside > div > div > div > div'
                ' > div:nth-child(3) > span.app-checkbox__text.is-clickable'
            )
        )
        availability_check.click()
        time.sleep(TIME_DELAY)
    except Exception:
        logger.error('возникла ошибка в get_center()', exc_info=True)


def get_source_html(url: str, center: str, city: str) -> None:
    """Получаем полный html код страницы по заданному url"""
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url=url)
        get_city(driver, CITIES[city])
        get_center(driver, ALL_CENTERS[city][center])
        open_all_pages(
            driver,
            get_num_of_pages(driver),
            city,
            center
        )

    except Exception:
        logger.error('возникла ошибка', exc_info=True)
    finally:
        driver.close()
        driver.quit()
