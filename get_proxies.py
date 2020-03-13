from selenium.webdriver import PhantomJS as Browser
import json
import time
import re

proxy_list_url = "http://spys.one/socks/"
proxies = []
br = Browser()
br.get(proxy_list_url)
sizes = [25, 50, 100, 200, 300, 500]
pattern = re.compile(r"[.\s]+\((\d+)\)")
for country_id in range(1, 171):
    try_counter = 0
    count = 0
    while (elm := br.find_element_by_id('tldc')).find_element_by_xpath(f"./option[@selected]").get_attribute(
            "value") != str(country_id):
        elm = elm.find_element_by_xpath(f'./option[@value="{country_id}"]')
        elm.click()
        try_counter += 1
        if try_counter >= 2:
            break
    if try_counter >= 2:
        continue
    count = int(pattern.findall(elm.text)[0])
    key = 0
    for key, size in enumerate(sizes):
        if int(size) > count:
            break
    try_counter = 0
    while (elm := br.find_element_by_id("xpp")).find_element_by_xpath("./option[@selected]").get_attribute(
            "value") != str(key):
        elm = elm.find_element_by_xpath(f'./option[@value="{key}"]')
        elm.click()
        try_counter += 1
        if try_counter >= 5:
            break
    if try_counter >= 5:
        continue
    elms = br.find_elements_by_class_name("spy1xx")[1:] + br.find_elements_by_class_name("spy1x")[1:]
    i = 0
    start = time.time()
    for elm in elms:
        tds = elm.find_elements_by_tag_name("td")
        proxies.append(dict(proxie_url=tds[0].text, type=tds[1].text, delay=float(tds[5].text)))
        i += 1
        if i % 50 == 0:
            stop = time.time()
            print(stop - start)
            start = stop
proxies.sort(key=lambda x: x['delay'])
with open("proxies.json", "w") as f:
    json.dump(proxies, f)
