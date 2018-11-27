#!/usr/bin/python3

# -*- encoding=utf8 -*-



import time, datetime



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





class KSEDAgreement(PageObject):



    mode = PageElement(xpath='//button[contains(@id, "default-cntrl-split-panel-button-button")]')

    fileUpload = PageElement(xpath='(//button[contains(@id, "fileUpload-button-button")])[2]')

    files = PageElement(xpath='//input[@type="file"][@name="files[]"]')


    show_main = PageElement(xpath='//a[contains(@id, "action-show-main")]')

    points = PageElement(xpath='//em[contains(text(), "Пункты")]')

    btnPoint = PageElement(xpath='//button[contains(@id, "create-point-button")]')

    Instr = PageElement(xpath='(//a[contains(@class, "yuimenuitemlabel")][contains(text(), "Поручение")])[1]')

    TextInstr = PageElement(xpath='//textarea[contains(@id, "point-desc")][contains(@name, "point-desc")]')

    type_point = PageElement(xpath='//input[contains(@id, "ts_type-assoc-cntrl-autocomplete")]')

    Responsible_executor = PageElement(xpath='//input[contains(@id, "ts_executor-assoc-cntrl-autocomplete")]')

    term = PageElement(xpath='//input[contains(@id, "ts_limitation-date-cntrl-date")]')

    btnForm_ok = PageElement(xpath='//button[contains(@id, "form-submit-button")]')

    sendFor_approval = PageElement(xpath='// div[contains(text(), "Направить на согласование")]')#// div[contains( @ id, "actions")]

    fileYes = PageElement(xpath='//a[contains(text(), "test.txt")]')

    heading_inf = PageElement(xpath='//h2[contains(@id, "heading")][contains(text(), "Основные сведения")]')

    status_Doc = PageElement(xpath='//span[contains(@id, "_status")]')


    def __init__(self, web_driver, uri=''):

        super().__init__(web_driver, uri)



    def addPoruchenie(self,):

        self.show_main.click()

        self.points.click()
        time.sleep(0.5)

        self.btnPoint.click()

        self.Instr.click()
        time.sleep(0.6)

        self.TextInstr.send_keys("Произвольный текст")

        self.type_point.send_keys("Поручение по пункту РД для сведения")
        self.type_point.send_keys(Keys.RETURN)

        self.Responsible_executor.send_keys("Главный")
        self.Responsible_executor.send_keys(Keys.RETURN)

        dd = datetime.date.today().strftime('%d%m%Y')
        self.term.send_keys(dd)
        time.sleep(0.5)

        self.btnForm_ok.click()
        time.sleep(0.8)

    def attachment(self,):

        self.mode.click()
        time.sleep(3)
        self.fileUpload.click()
        time.sleep(2)
        self.files.send_keys('C://test.txt')

        assert "test.txt" in self.fileYes
        time.sleep(0.5)


    def Agreement(self,):

        self.sendFor_approval.click()

        wait_page_loaded(self.w)
        time.sleep(4)

        # Проверим статус документа
        self.heading_inf.click()
        time.sleep(0.5)
        assert "На согласовании" in self.status_Doc