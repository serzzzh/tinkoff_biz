import datetime
import json
import sys
import os
import re
from es_selenium import *


def main_list():
    sleep = 4
    old_operation_category = None  # 'Возврат средств'
    new_operation_category = 'Выручка от контрагента'
    el_regexp_search = 'ПАО КБ "УБРиР"'
    # '(Московский банк Сбербанка России)|(Возврат средств)'



    driver = load_driver(browser='Chrome')  # Chrome IE
    go_url('https://accounting.tinkoff.ru/feed/any')
    input('pass...?')

    for el in find_elements(By.CSS_SELECTOR, '.content.ng-untouched.ng-pristine.ng-valid'):
        if not re.search(el_regexp_search, el.get_attribute('outerHTML')) is None:
            try:
                el.click()
            except Exception as e:
                ...

            # смена указанной категории
            if old_operation_category is not None \
                    and check_element_exists(By.XPATH, f"//input[@value='{old_operation_category}']"):
                if not click(By.XPATH, f"//input[@value='{old_operation_category}']"):
                    ...
                if not click(By.XPATH, f"//span[contains(text(), '{new_operation_category}')]"):
                    ...
                if not click(By.XPATH, "//button[@automation-id='save-button']"):
                    ...
                time.sleep(sleep)

            # выставление новой категории
            while old_operation_category is None:
                el = driver.find_elements(By.XPATH, '//input[@automation-id="select-field-input"]')[2]
                if el is None:
                    break
                el.click()

                if not click(By.XPATH, f"//span[contains(text(), '{new_operation_category}')]"):
                    ...
                if not click(By.XPATH, "//button[@automation-id='save-button']"):
                    ...
                time.sleep(sleep)
    print('ok')


def main():
    sleep = 4
    driver = load_driver(browser='Chrome')  # Chrome IE
    go_url('https://accounting.tinkoff.ru/accounting/prepayments/%D0%93%D0%94.00.2018/taxBase')
    input('pass...?')

    input_value = 'Возврат средств'
    for el in find_elements(By.CLASS_NAME, 'ui-ticker'):
        if el.text == 'Московский банк Сбербанка России':  # ПАО КБ "УБРиР"
            try:
                el.click()
            except Exception as e:
                ...

            if check_element_exists(By.XPATH, f"//input[@value='{input_value}']"):
                if not click(By.XPATH, f"//input[@value='{input_value}']"):
                    ...
                if not click(By.XPATH, "//span[contains(text(), 'Выручка от контрагента')]"):
                    ...

                if not click(By.XPATH, "//button[@automation-id='save-button']"):
                    ...
                time.sleep(sleep)
    print('ok')

if __name__ == '__main__':
    main_list()