#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time


import pickle
from selenium.webdriver import ActionChains

from page_objects import PageObject

from page_objects import PageElement

from page_objects import MultiPageElement

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import urllib.request, requests





def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)





class KSEDallureTest(PageObject):



    username_text = PageElement(name='username')

    password_text = PageElement(name='password')

    LogIn_button = PageElement(xpath='//span/button')

    allur = PageElement(xpath='//div[contains(text(), "Отчеты")]')

    node_Statis = PageElement(xpath='//span[contains(@class, "ygtvlabel")][contains(text(), "Статистические")]')

    stat_tipDoc = PageElement(xpath='//a[contains(text(), "Сводка по типам документов")]')

    btnOK = PageElement(xpath='//button[contains(@id, "reportForm-form-submit-button")]')



    def __init__(self, web_driver, uri=''):

        super().__init__(web_driver, uri)

  #      self.get('http://213.128.208.34/share/page/arm?code=SED')

        wait_page_loaded(self.w)



    def openAllure(self,):

        self.allur.click()
        time.sleep(1)
        self.node_Statis.click()
        time.sleep(1)
        self.stat_tipDoc.click()
        time.sleep(2)

        pageH_url = self.w.current_url # урл текущей страницы

        self.btnOK.click()
        time.sleep(3)

        r = requests.get(pageH_url)
        cookies = r.cookies
        #cookies = dict(cookies_are='working')
        pickle.dump(self.w.get_cookies(), open("cookies.pkl", "wb"))

        current = self.w.current_window_handle

        newWindow = [window for window in self.w.window_handles if window != current][0]
        self.w.switch_to.window(newWindow)

        page_url = self.w.current_url # урл нового окна
        r = requests.get(page_url)
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.w.add_cookie(cookie)
            r = requests.get(page_url)

        my_file = open("some.txt", "w")
        my_file.write(str(r.status_code))
        my_file.close()
        #r = requests.get(page_url, cookies=cookies)
        #code = str(r.text())
        #print(str(r.status_code))
