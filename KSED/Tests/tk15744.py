#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time, datetime

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

from KSED.Pages.PageObject import Locator
from KSED.TestData.data import dataTest
from KSED.TestData.locators import KSEDLocators
from KSED.pages import MPages, WebPage




def wait_page_loaded(driver):

    time.sleep(2)

    page_loaded = False



    while not page_loaded:

        page_loaded = driver.execute_script("return document.readyState == 'complete';")

        time.sleep(0.1)

class KSEDaddPerson(MPages, dataTest, KSEDLocators):

    def __init__(self, web_driver, uri=dataTest.baseURL):

        super().__init__(web_driver, uri)


    # Авторизация
    def LogIN(self, username, password):

        self.username_text = username
        self.password_text = password
        self.LogIn_button.click()
        self.wait_page_loaded()

        assert "АРМ" in self._web_driver.title

    #открытие документа
    def getDoc(self):

        my_file = open("Tests/linkDocCS.txt", "r")
        my_string = my_file.read()
        my_string.strip()
        self._web_driver.get(my_string)
        my_file.close()

    def creation_of_the_approval_route(self):

        # "Согласование" вкладка
        self.soglasovanieWkladka.wait_to_be_clickable()
        self.soglasovanieWkladka.click()


        # time.sleep(2)
        # self.navedenieSogl.move_to_element()
        # выпадающий список согласований
        self.dropBtn_2.scroll_to_element()
        self.dropBtn_2.wait_to_be_clickable()
        self.dropBtn_2.click()
        # Добавление сотрудника
        self.btnAddPerson.wait_to_be_clickable()
        self.btnAddPerson.click()

        self.btnSelection_3.wait_to_be_clickable()
        self.btnSelection_3.click()  # кнопка + третий выбор

        self.confirm_5.wait_to_be_clickable()
        self.confirm_5.click()  # кнопка подтвердить
        time.sleep(5)

        # # "Создать маршрут" клик по кнопке
        # self.createRuleBtn.wait_to_be_clickable()
        # self.createRuleBtn.click()

        # # Выберем "Индивидуальный маршрут"
        # self.createRuleIndivid.wait_to_be_clickable()
        # self.createRuleIndivid.click()
        #
        # # Появилась форма "Редактирование маршрута" нажмем "ОК"
        # self.btnOKform.wait_to_be_clickable()
        # self.btnOKform.click()

        # # Нажмем кнопку "Добавить этап"
        # self.addEtap.wait_to_be_clickable()
        # self.addEtap.click()

        # # Заполним "Вид этапа"
        #
        # self.btnTree.wait_to_be_clickable()
        # self.btnTree.click()  # нажать на кнопку ...
        #
        # self.btnSelection3.wait_to_be_clickable()
        # self.btnSelection3.click()  # кнопка + третий выбор
        #
        # self.confirm_5.wait_to_be_clickable()
        # self.confirm_5.click()  # кнопка + третий выбор
        #
        # # Заполним "Согласующие"
        # self.soglasuychie.wait_until_not_visible()
        # self.soglasuychie.send_keys("Яцкин" + Keys.RETURN)


        # # Нажмем кнопку "ОК" на форме
        #
        # self.btnOKformSogl.scroll_to_element()
        # self.btnOKformSogl.wait_to_be_clickable()
        # self.btnOKformSogl.click()
        # self.wait_page_loaded(wait_for_xpath_to_disappear='//div[@id="confirm-edit-fields-form-container_mask"]')

    #     # выпадающий список согласований
    #     self.dropBtn_2.wait_to_be_clickable()
    #     self.dropBtn_2.click()
    #
    #
    #
    #     self.status_Doc.wait_until_not_visible()
    #     assert "Не начато" in self.resultSogl.get_text() #----- проверка не корректная
    #
    # # Сохраним ссылку на документ в файл
    # def LinkDocWFile(self):
    #
    #     url = self._web_driver.current_url
    #     my_file = open("Tests/linkDocCS.txt", "w")
    #     my_file.write(str(url))
    #     my_file.close()

