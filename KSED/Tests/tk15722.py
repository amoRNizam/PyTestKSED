#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time, datetime

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys

from KSED.TestData.data import dataTest
from KSED.TestData.locators import KSEDLocators
from KSED.TestData.pages import MPages

import allure
def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)

class KSEDCreatDocCS_LND(MPages, dataTest, KSEDLocators):

    def __init__(self, web_driver, uri=dataTest.baseURL):

        super().__init__(web_driver, uri)


    @allure.step("Авторизация")
    def LogIN(self, username, password):

        self.username_text = username
        self.password_text = password
        self.LogIn_button.click()
        self.wait_page_loaded()

        assert "АРМ" in self._web_driver.title

    @allure.step("Создание документа (открытие формы создания и заполнение атрибутов)")
    def Creat(self,):

        wait = WebDriverWait(self._web_driver, 10)

        self.newDoc_button.click()

        self.cardSogl.click()

        self.wait_page_loaded()

        assert "Страница создания документа" in self._web_driver.title

        # Атрибуты документа
        self.wait_page_loaded()
        # Куратор
        self.kurator.wait_until_not_visible()
        self.kurator.scroll_to_element()
        self.kurator.send_keys(u'Яцкин' + Keys.ENTER)


        # Вид документа
        self.viewSelecton.wait_until_not_visible()
        self.viewSelecton.wait_to_be_clickable()
        self.viewSelecton.click()

        # Выбор ЛНД
        self.lndSelecton.wait_until_not_visible()
        self.lndSelecton.wait_to_be_clickable()
        self.lndSelecton.click()

        # Выбор раздела из ЛНД
        self.btnSelection3.wait_to_be_clickable()
        self.btnSelection3.click()

        # кнопка подтвердить
        self.confirm_6.wait_to_be_clickable()
        self.confirm_6.click()

        # Подписант
        self.podpisanti.wait_until_not_visible()
        self.podpisanti.scroll_to_element()
        self.podpisanti.send_keys(u'Иванов2' + Keys.ENTER)


        # процессы верхнего уровня
        self.proUpLevel.wait_until_not_visible()
        self.proUpLevel.wait_to_be_clickable()
        self.proUpLevel.click()

        # Выбор процесса
        self.btnSelection_5.wait_to_be_clickable()
        self.btnSelection_5.click()

        # кнопка подтвердить
        self.confirm_7.wait_to_be_clickable()
        self.confirm_7.click()

        # вид ЛНД

        self.levelFirst_1.wait_until_not_visible()
        self.levelFirst_1.scroll_to_element()
        self.levelFirst_1.send_keys(u'Политика' + Keys.ENTER)

        # self.viewLndSelecton.wait_until_not_visible()
        # self.viewLndSelecton.wait_to_be_clickable()
        # self.viewLndSelecton.click()

        # # Выбор уровня

        # self.levelFirst.move_to_element()
        # self.levelFirst.wait_to_be_clickable()
        # self.levelFirst.click()

        # self.wait_page_loaded()

        # # Выбор процесса
        # self.btnSelection_4.move_to_element()
        # self.btnSelection_4.wait_to_be_clickable()
        # self.btnSelection_4.click()

        # # кнопка подтвердить
        # self.confirm_8.wait_to_be_clickable()
        # self.confirm_8.click()

        # заголовок
        dt = datetime.datetime.today().strftime("%m-%d-%H.%M.%S")
        self.titleCS.scroll_to_element()
        self.titleCS.send_keys(u'Auto ЛНД 15722 ' + dt)

        # кнопка сохранить проект
        self.saveProject.wait_to_be_clickable()
        self.saveProject.click()
        self.wait_page_loaded(wait_for_xpath_to_disappear='//div[@id = "message"]//span[@class = "wait"]')
        self.wait_page_loaded()
        assert "Документ" in self._web_driver.title


    #
    # # Сохраним ссылку на документ в файл
    # def LinkDocWFile(self):
    #
    #     url = self._web_driver.current_url
    #     my_file = open("Tests/linkDocPoruchenie.txt", "w")
    #     my_file.write(str(url))
    #     my_file.close()

