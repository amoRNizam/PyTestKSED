#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time, datetime


from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import *

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

from Pages.PageObject import Locator
from TestData.data import dataTest
from TestData.locators import KSEDLocators





def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)




class KSEDDocPorSendAllure(Locator, dataTest, KSEDLocators):


    def __init__(self, web_driver, uri=''):

        super().__init__(web_driver, uri)

        self.get(dataTest.baseURL)

        wait_page_loaded(self.w)

    # Авторизация
    def LogIN(self, username, password):
        # wait = WebDriverWait(self.w, 10, poll_frequency=1,
        #                      ignored_exceptions=[NoSuchElementException,
        #                                          ElementNotVisibleException,
        #                                          ElementNotSelectableException])
        page = Locator(self.w)

        page.username_text = username
        print(Locator.username_text)
        page.password_text = password

        page.LogIn_button.click()

        wait_page_loaded(self.w)

        assert "АРМ" in self.w.title


    # Открытие документа из прошлого ТК
    def getDoc(self):

        self.w.get(KSEDLocators.LinkDoc)
        wait_page_loaded(self.w)

    # Отправка отчета
    def sendAllure(self, ):

        page = Locator(self.w)

        wait = WebDriverWait(self.w, 10)

        # Кликнем по действию "Отправить отчет" в функциональном меню "Действия"
        time.sleep(1)
        page.actionSendAllere.click()

        # Заполним поле "Текст отчета"
        WebDriverWait(self.w, 10).until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.textAllur)))
        page.textAllur.click()

        # Добавим связь с документом
        page.btnAddSvyz.click()

        time.sleep(0.5)
        page.searchDoc.send_keys("У" + Keys.RETURN)

        time.sleep(1)

        page.oneListEl.click()

        page.btnOK.click()

        # Нажмем кнопку "Отправить"
        WebDriverWait(self.w, 10).until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.btnSend)))
        page.btnSend.click()

        wait_page_loaded(self.w)

        # Проверим статус документа
        wait.until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.osnSvedeniya)))
        page.osnSvedeniya.click()

        assert "Исполнено" in self.status_Doc.text

    # # Сохраним ссылку на документ в файл
    # def LinkDocWFile(self):
    #
    #     url = self.w.current_url
    #     my_file = open("TestData\linkDoc.txt", "w")
    #     my_file.write(str(url))
    #     my_file.close()
