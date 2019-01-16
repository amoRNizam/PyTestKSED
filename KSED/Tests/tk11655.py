#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time, datetime



from selenium.webdriver import ActionChains

from page_objects import PageObject

from page_objects import PageElement

from page_objects import MultiPageElement

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import *

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

from KSED.Pages.PageObject import Locator
from KSED.TestData.data import dataTest
from KSED.TestData.locators import KSEDLocators
from KSED.pages import MPages




def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)




class KSEDCreatDocPor(Locator, dataTest, KSEDLocators):


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
        #**page = MPages(self.w, self.w.current_url)

        page.username_text = username
        print(Locator.username_text)
        page.password_text = password

        page.LogIn_button.click()

        wait_page_loaded(self.w)

        assert "АРМ" in self.w.title

    # Создание документа (открытие формы создания и заполнение атрибутов)
    def Creat(self,):
        # wait = WebDriverWait(self.w, 10, poll_frequency=1,
        #                      ignored_exceptions=[NoSuchElementException,
        #                                          ElementNotVisibleException,
        #                                          ElementNotSelectableException])

        page = Locator(self.w)
        #page = MPages(self.w, self.w.current_url)

        wait = WebDriverWait(self.w, 10)

        page.newDoc_button.click()

        page.poruchenie.click()

        #**page.wait_page_loaded()
        wait_page_loaded(self.w)
        assert "Страница создания документа" in self.w.title

        time.sleep(3)
        # Атрибуты документа
        wait_page_loaded(self.w)
        #**page.wait_page_loaded()
        # Тип поручения
        wait.until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.tipPoruch)))
        self.w.execute_script("arguments[0].scrollIntoView();", page.tipPoruch)
        page.tipPoruch.send_keys(u'Для информации' + Keys.RETURN)
        #page.tipPoruch.send_keys(Keys.RETURN)
        time.sleep(2)
        # Категория документа
        wait.until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.category_doc)))
        page.category_doc.send_keys(u'Открытый' + Keys.RETURN)

        # Ответственный исполнитель
        self.w.execute_script("arguments[0].scrollIntoView();", page.otvetstv_ispoln)
        #**page.otvetstv_ispoln.scroll_to_element()
        page.otvetstv_ispoln.send_keys(u'Строганов' + Keys.RETURN)

        time.sleep(1)

        # Кнопка "Создать"
        self.w.execute_script("arguments[0].scrollIntoView();", page.btnCreateDoc)
        #**page.btnCreateDoc.scroll_to_element()
        wait.until(EC.element_to_be_clickable((By.XPATH, KSEDLocators.btnCreateDoc)))
        page.btnCreateDoc.click()

#        wait.until(EC.number_of_windows_to_be(2))

        wait_page_loaded(self.w)
#        self.w.set_page_load_timeout(30)
        time.sleep(3)

#
#        wait.until(EC.title_is(self.w.title))

        assert "Документ" in self.w.title


    # Сохраним ссылку на документ в файл
    def LinkDocWFile(self):

        url = self.w.current_url
        my_file = open("Tests/linkDocPoruchenie.txt", "w")
        my_file.write(str(url))
        my_file.close()

    # def getDoc(self):
    #
    #     self.w.get(KSEDLocators.LinkDoc)
