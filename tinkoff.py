import datetime
import json
import sys
import os
import re
from es_selenium import *


def main_list():
    sleep = 4
    # 'Возврат средств' 'Выручка от контрагента'
    old_operation_category = None
    # 'Выручка через агента'  'Эквайринг'
    new_operation_category = 'Расходы по ведению деятельности'
    #   'ООО "СДЭК-ДС"'
    contragent = 'СЕТЬ'
    # '(Московский банк Сбербанка России)|(Возврат средств)'

    str_category = '//input[@_ngcontent-c51=""][@placeholder=""]'

    driver = load_driver(browser='Chrome')  # Chrome IE
    go_url('https://accounting.tinkoff.ru/feed/any')
    input('pass...?')
    ...
    while True:
        try:
            record = find_elements(By.CSS_SELECTOR, '.content.ng-untouched.ng-pristine.ng-valid')[0]
            record.click()
        except Exception as e:
            ...
        # if not re.search(contragent, record.get_attribute('outerHTML')) is None:


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
        if old_operation_category is None:
            el = find_element(By.XPATH, str_category)
            el.click()

            if not check_element_exists(By.XPATH, f"//span[contains(text(), '{new_operation_category}')]"):
                #  меняем стиль элемента, чтобы показать все значения списка
                st = find_element(By.CSS_SELECTOR, "head > style:nth-child(60)")
                driver.execute_script("var el=arguments[0]; el.innerHTML = "
                                      "el.innerHTML.replace('max-height:250px', 'max-height:550px');", st)
                el = find_element(By.XPATH, str_category)
                el.click()
                el.click()

            if not click(By.XPATH, f"//span[contains(text(), '{new_operation_category}')]"):
                ...

            if new_operation_category == 'Эквайринг':
                el_amount = find_element(By.XPATH, "//ng2-money[@automation-id='amount']")
                base_amount = el_amount.find_element(By.XPATH, './/span[@automation-id="base-part"]').text.replace(" ", "")
                decimal_amount = el_amount.find_element(By.XPATH, './/span[@automation-id="decimal-part"]').text.replace(" ₽", "")
                amount = base_amount + decimal_amount
                el_input = find_element(By.XPATH,
                                        '//input[@_ngcontent-c52=""][@automation-id="input"][@placeholder=""]')
                el_input.send_keys(amount)
                time.sleep(0.3)
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