import logging
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException


page_load_timeout = 3  # 1-2-3-4-5 sec


def find_element(method, html_element):
    for time_wait in range(page_load_timeout):
        if check_element_exists(method, html_element):
            element = driver.find_element(method, html_element)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            return element
        else:
            driver.implicitly_wait(time_wait)
    return None


def find_elements(method, html_element):
    for time_wait in range(page_load_timeout):
        if check_element_exists(method, html_element):
            elements = driver.find_elements(method, html_element)
            # actions = ActionChains(driver)
            # actions.move_to_element(element).perform()
            return elements
        else:
            driver.implicitly_wait(time_wait)
    return None


def send_keys(method, html_element, text):
    try:
        wait_element(method, html_element)
        element = find_element(method, html_element)
        if element is not None:
            # driver.execute_script("arguments[0].value = arguments[1]", element, text)
            element.send_keys(text)
            return True
        else:
            return False
    except Exception as e:
        return False


def get_element_text(method, html_element):
    try:
        element = find_element(method, html_element)
        if element is not None:
            return element.text
        else:
            return False
    except Exception as e:
        return False


def click(method, html_element):
    try:
        wait_element(method, html_element)
        element = find_element(method, html_element)
        if element is not None:
            element.click()  # it's not working stable
            # element.send_keys("\n") #  it's not working stable
            return True
        else:
            return False
    except Exception as e:
        return False


def click_url(method, html_element):
    try:
        wait_element(method, html_element)
        element = find_element(method, html_element)
        if element is not None:
            element.click()  # it's not working stable
            # element.send_keys("\n")
            return True
        else:
            return False
    except Exception as e:
        return False


def click_wait(method, html_element, wait_time=page_load_timeout):
    if wait_element(method, html_element, wait_time):
        if click(method, html_element):
            return True
    return False


def wait_element(method, html_element, wait_time=page_load_timeout):
    for wait_sec in range(wait_time):
        try:
            WebDriverWait(driver, wait_sec).until(EC.element_to_be_clickable((method, html_element)))
            return True
        except Exception as e:
            ...
    return False


def wait_while_exists(method, html_element, value='', wait_time=page_load_timeout):
    for wait_sec in range(wait_time):
        try:
            if check_element_exists(method, html_element):
                time.sleep(wait_time)
            else:
                return True
        except Exception as e:
            ...
    return False


def check_element_exists(method, html_element):
    try:
        driver.implicitly_wait(0.5)
        driver.find_element(method, html_element)
        return True
    except Exception as e:
        return False


def check_elements_exists(method, html_element):
    try:
        driver.implicitly_wait(0.5)
        driver.find_elements(method, html_element)
        return True
    except Exception as e:
        return False


def go_url(link, go_url_page_load_timeout=page_load_timeout):
    try:
        driver.set_page_load_timeout(go_url_page_load_timeout)
        driver.implicitly_wait(3)
        driver.get(link)
        driver.implicitly_wait(go_url_page_load_timeout)
    except Exception as e:
        try:
            driver.get(link)
        except:
            pass
    finally:
        driver.set_page_load_timeout(page_load_timeout)
        driver.implicitly_wait(go_url_page_load_timeout)


def open_wait(link, wait_title='', go_url_page_load_timeout=page_load_timeout):
    try:
        driver.get(link)
        if not wait_title:
            for wait_time in range(go_url_page_load_timeout):
                if wait_title == driver.title:
                    return True
    finally:
        return f"Can't open URL: {link}"


def mouse_click(html_element, x_offset, y_offset, action='xpath'):
    method = ACTIONS.get(action, False)
    callback = getattr(driver, method)
    if callback:
        try:
            el = callback(html_element)
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(el, x_offset, y_offset)
            action.click()
            action.perform()
            return True
        except Exception as e:
            # print('err: ' + str(e))
            return False
    else:
        raise AttributeError("No such action.")


def load_driver(browser='Chrome'):
    global driver
    if browser == 'IE':
        driver = webdriver.Ie("./IEDriverServer32.exe",
                              capabilities={'ignoreZoomSetting': True, 'detach': True, 'requireWindowFocus': True,
                                            'ensureCleanSession': True,
                                            'INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS': True})

        driver.execute_script("document.body.style.zoom='zoom %'")
        driver.maximize_window()

        # file = open('config.ini', 'w')
        # file.write(driver.command_executor._url + ',' + driver.session_id)
        # file.close()

    if browser == 'Chrome':
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        # options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        driver.maximize_window()
        driver.set_page_load_timeout(page_load_timeout)

    if browser == 'PhantomJS':
        driver = webdriver.PhantomJS("./phantomjs.exe")

    return driver


def send_mail(mail_from, mail_to, subj, body):
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subj
    msg['From'] = mail_from
    msg['To'] = mail_to

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Send the message via our own SMTP server, but don't include the envelope header.
    conn = smtplib.SMTP(SMTP_SERVER, 587)
    conn.set_debuglevel(False)
    conn.ehlo()
    conn.starttls()
    conn.ehlo()
    conn.login(DOMAIN + '\\' + MAIL_USER, MAIL_PASSWORD)
    try:
        conn.sendmail(mail_from, mail_to, msg.as_string())
    finally:
        conn.quit()


def wheel_element(element, deltaY=120, offsetX=0, offsetY=0):
    error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }    
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
    if error:
        raise WebDriverException(error)
