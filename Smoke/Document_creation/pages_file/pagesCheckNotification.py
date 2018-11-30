#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time



from selenium.webdriver import ActionChains

from page_objects import PageObject

from page_objects import PageElement

from page_objects import MultiPageElement

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys





def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)





class KSEDNotificationOfDecision(PageObject):



    username_text = PageElement(name='username')

    password_text = PageElement(name='password')

    LogIn_button = PageElement(xpath='//span/button')

    notif = PageElement(id_='NOTIFICATIONS_text')

    notif_2 = PageElement(xpath='(//div[contains(@class, "notification-row")]//*[contains(text(), "Принято решение")])')

    notifClick = PageElement(xpath='//div[contains(@class, "notification-row")]')

    approved = PageElement(xpath='//button[contains(@id, "APPROVED-button")]')

    comment = PageElement(name='prop_bpm_comment')

    applyBtn_ok = PageElement(xpath='//button[contains(@id, "set-apply-button-button")]')









    def __init__(self, web_driver, uri=''):

        super().__init__(web_driver, uri)

        self.get('http://213.128.208.34/share/page/arm?code=SED')

        wait_page_loaded(self.w)



    def LogIN(self, username, password):

        self.username_text = username

        self.password_text = password

        self.LogIn_button.click()


        wait_page_loaded(self.w)

        assert "АРМ" in self.w.title

    def Notification(self,):

        self.notif.click()


        self.w.execute_script("arguments[0].scrollIntoView();", self.notif_2)
#        self.notif_1.click()


        assert "Принято решение по документу" in self.notif_2.text



