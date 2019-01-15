
#!/usr/bin/python3
# -*- encoding=utf8 -*-

# TODO: write article about __elements nasledovanie hack.
# TODO: switch to iframe
# TODO: overlapping elements ???
# TODO: add right click

import time
from KSED.elements import WebElement, ManyWebElements

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from utils import KNOWN_JS_ISSUES
from KSED.TestData.locators import KSEDLocators

class WebPage(object):

    _web_driver = 'my web driver'

    def __init__(self, web_driver, url=''):
        self._web_driver = web_driver
        self.get(url)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self.__getattribute__(name)._set_value(self._web_driver, value)
        else:
            super(WebPage, self).__setattr__(name, value)

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if not item.startswith('_') and not callable(attr):
            attr._web_driver = self._web_driver

        return attr

    def get(self, url):
        self._web_driver.get(url)
        self.wait_page_loaded()

    def go_back(self):
        self._web_driver.back()
        self.wait_page_loaded()

    def refresh(self):
        self._web_driver.refresh()
        self.wait_page_loaded()

    def screenshot(self, file_name='screenshot.png'):
        self._web_driver.screenshot(file_name)

    def scroll_down(self, offset=0):
        """ Scroll the page down. """
        raise NotImplemented

    def scroll_up(self, offset=0):
        """ Scroll the page up. """
        raise NotImplemented

    def switch_to_iframe(self, iframe):
        """ Switch to iframe by it's name. """

        self._web_driver.switch_to.frame(iframe)

    def switch_out_frame(self):
        """ Cancel iframe focus. """
        self._web_driver.switch_to.default_content()

    def check_js_errors(self, ignore_list=None):
        """ This function checks JS errors on the page. """

        ignore_list = ignore_list or []

        logs = self._web_driver.get_log('browser')
        for log_message in logs:
            if log_message['level'] != 'WARNING':
                ignore = False
                for issue in ignore_list:
                    if issue in log_message['message']:
                        ignore = True
                        break

                assert ignore, 'JS error "{0}" on the page!'.format(log_message)

    def wait_page_loaded(self, timeout=60, check_js_complete=True,
                         check_page_changes=True, check_images=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear=''):
        """ This function waits until the page will be completely loaded.
            We use many different ways to detect is page loaded or not:

            1) Check JS status
            2) Check modification in source code of the page
            3) Check that all images uploaded completely
               (Note: this check is disabled by default)
            4) Check that expected elements presented on the page
        """

        page_loaded = False
        k = 0

        source = ''
        try:
            source = self._web_driver.page_source
        except:
            pass

        # Wait until page loaded (and scroll it, to make sure all objects will be loaded):
        while not page_loaded:
            time.sleep(0.1)
            k += 1

            if check_js_complete:
                # Scroll down and wait when page will be loaded:
                try:
                    self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    page_loaded = self._web_driver.execute_script("return document.readyState == 'complete';")
                except:
                    pass

            if page_loaded and check_page_changes:
                # Check if the page source was changed
                new_source = ''
                try:
                    new_source = self._web_driver.page_source
                except:
                    pass

                page_loaded = new_source == source
                source = new_source

            # Wait when spinner of page loading will disappear:
            if page_loaded and wait_for_xpath_to_disappear:
                bad_element = None

                try:
                    bad_element = WebDriverWait(self._web_driver, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, wait_for_xpath_to_disappear))
                    )
                except:
                    pass  # Ignore timeout errors

                page_loaded = not bad_element

            if page_loaded and wait_for_element:
                try:
                    page_loaded = WebDriverWait(self._web_driver, 0.1).until(
                        EC.element_to_be_clickable(wait_for_element._locator)
                    )
                except:
                    pass  # Ignore timeout errors

            assert k < timeout, 'The page loaded more than {0} seconds!'.format(timeout)

        # Go up:
        self._web_driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')


class WebPageDA(WebPage):

    sort_by_times_seen = WebElement(xpath='//span[contains(text(), "Times Seen")]')
    table_data_cells = ManyWebElements(xpath='//*[contains(@class, "-ad-cell-") or contains(@class, '
                                             '"ad-cell__number") or contains(@class, "ad-cell__date")]')
    table_data_text_fields = ManyWebElements(xpath='//*[contains(@class, "asns-text-ad-item")]//span')
    next_button = WebElement(xpath='//span[text()="Next"]')
    search_field = WebElement(xpath='//s-input')
    show_advanced_filters = WebElement(xpath='//span[contains(text(), "Advanced filters")]')
    search_button = WebElement(xpath='//button[contains(@class, "s-btn -hollow")]')
    filter_by = WebElement(xpath='//div[text()="Ad"]')
    filter_method = WebElement(xpath='//div[text()="Text Contains"]')
    advanced_filter_text = WebElement(xpath='//input[@placeholder="Text"]')
    apply_filter_button = WebElement(xpath='//span[text()="Apply Filters"]')
    add_one_more_filter_button = WebElement(xpath='//span[text()="Add one more"]')
    first_advanced_filter = WebElement(xpath='(//div[contains(@class, "item__layout")])[1]//input')
    second_advanced_filter = WebElement(xpath='(//div[contains(@class, "item__layout")])[2]//input')
    ads_tab = WebElement(xpath='//span[text()="Ads"]')
    ads_main_numbers = ManyWebElements(xpath='//*[@class="asns-legend__number"]')
    image_ads_tab = WebElement(xpath='//span[contains(text(), "Image ")]')
    landing_pages_tab = WebElement(xpath='//span[text()="Landing Pages"]')
    text_ads_tab = WebElement(xpath='//span[contains(text(), "Text ")]')
    html_ads_tab = WebElement(xpath='//span[contains(text(), "HTML ")]')
    export_button = WebElement(xpath='(//span[text()="Export"])[1]')
    last_page_link = WebElement(xpath=('//span[contains(@class, "pagination__last-item")]//'
                                       'span[contains(@class, "link__content")]'))
    last_page_text = WebElement(xpath='//span[contains(@class, "pagination__last-item")]')
    all_ads = ManyWebElements(xpath='//tr[@class="asns-table-creative-row"]')
    ads_links = ManyWebElements(xpath='//td/a|//td/div/a')
    role_switcher = WebElement(xpath='//button[contains(@class, "platform_select")]')
    role_advertiser = WebElement(xpath='//div[text()="advertiser"]')
    role_publisher = WebElement(xpath='//div/div[contains(text(), "publisher")]')
    role_current = WebElement(xpath='(//button/div[contains(@class, "-select-trigger-label")])[1]')
    period_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[3]')
    device_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[2]')
    country_filter = WebElement(xpath='(//span[contains(@class, "Styles__filterCaption")])[1]')
    period_all_time = WebElement(xpath='//span[text()="All Time"]')
    device_desktop = WebElement(xpath='//span[text()="Desktop"]')
    country_us = WebElement(xpath='//span[text()="United States"]')
    overview_image_ads_links = ManyWebElements(xpath='//a[contains(@class, "MediaItemStyles__item_ad_link")]')
    overview_html_ads_links = ManyWebElements(xpath='//a[contains(@class, "InfoStyles__item_ad_link")]')
    overview_text_ads_links = ManyWebElements(xpath='//div[contains(@class, "TextItemStyles__info_link")]/a')
    overview_all_titles = ManyWebElements(xpath='//div[@type="secondary"]')
    landing_fast_link = WebElement(xpath='(//div[@type="primary"]/a)[1]')
    landing_ads_examples = ManyWebElements(xpath='//div[contains(@class, "NoDataSamplesLoop__ad_")]')
    creative_target_url = WebElement(xpath='//div[@class="asns-creative-target-url"]')
    next_ads = WebElement(xpath='//div[contains(@class, "creative-popup__next")]')
    advertisers_links = ManyWebElements(xpath='//a[@class="asns-js-cross-link asns-publisher-detail"]')
    overview_main_info = WebElement(xpath='//div[contains(@class, "OverviewLayoutStyles__ranks")]')
    cross_ads_count_links = ManyWebElements(xpath='//a[@class="asns-publisher-link asns-js-cross-link"]')
    cross_image_ads = ManyWebElements(xpath='//img[@class="asns-table-media-ad-cell__image"]')
    cross_table_lines = ManyWebElements(xpath='//*[contains(@class,"asns-table-media-ad-cell__preview")]')
    export_type_first = WebElement(xpath='(//button[contains(@class, "exportTo")])[1]')
    keywords_advertiser_links = ManyWebElements(xpath='//tr/td[2]//a[contains(text(),".")]')
    upgrade_to_business_button = ManyWebElements(xpath='//span[text()="Upgrade to Business"]')
    see_all_features_links = ManyWebElements(xpath='//a[text()="See all features"]')
    upgrade_links = ManyWebElements(xpath='//span[text()="Upgrade"]')
    ads_count = WebElement(xpath='(//div//h4//span)[1]')
    pubs_count = WebElement(xpath='(//div//h4//span)[2]')
    times_seen_info = WebElement(xpath='(//div//h4//span)[3]')
    first_seen_info = WebElement(xpath='(//div//h4//span)[4]')
    last_seen_info = WebElement(xpath='(//div//h4//span)[5]')
    contries_list = ManyWebElements(xpath='//div[contains(@class, "legend_country")]/div')
    contries_percents = ManyWebElements(xpath='//div[contains(@class, "legend_percent")]/div')
    countries_numbers = ManyWebElements(xpath='//div[contains(@class, "legend_total")]/div')
    ad_types = ManyWebElements(xpath='//div[contains(@class, "AdTypeChartStyles__ad_type")]//span')
    devices_types = ManyWebElements(xpath='//div[contains(@class, "DeviceStyles__device")]//span')
    domains_list = ManyWebElements(xpath=('//div[contains(@class, "TableStyles__table_row__item")]'
                                          '//a[contains(text(), ".")]'))
    publishers_data = ManyWebElements(xpath='//div[contains(@class, "TableStyles__table_row__item")]//span')
    ads_tab_main_numbers = ManyWebElements(xpath='//*[contains(@class, "asns-legend__number")]')
    ads_table_data = ManyWebElements(xpath='//td[contains(@class, "asns-table-media-ad-cell--text")]')

    # Landing page elements:
    landing_pages_titles = ManyWebElements(xpath='//div[contains(@class,"asns-landing-title")]')
    landing_pages_links = ManyWebElements(xpath='//div[contains(@class,"asns-landing-detail--url")]')
    table_data_ads_count = ManyWebElements(xpath='//td[@data-test="ads"]')
    table_data_times_seen = ManyWebElements(xpath='//td[@data-test="timesSeen"]')
    table_data_days_seen = ManyWebElements(xpath='//td[@data-test="daysSeen"]')


    check_pageobject = WebElement(xpath='(//*[@class, "profile-menu-item"])[0]')


    def wait_page_loaded(self, timeout=600, check_js_complete=True,
                         check_page_changes=True, check_images=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear=''):
        if not wait_for_xpath_to_disappear:
            super(WebPageDA, self).wait_page_loaded(timeout=timeout,
                wait_for_xpath_to_disappear='//*[contains(@class, "asns-spinner")]')
            # self.check_js_errors()

    def check_js_errors(self, ignore_list=None):
        if not ignore_list:
            super(WebPageDA, self).check_js_errors(ignore_list=KNOWN_JS_ISSUES)

    def search(self, search_query):
        self.search_field.click()
        element = self._web_driver.switch_to.active_element
        element.send_keys(search_query)
        self.search_button.click()
        self.wait_page_loaded()

    def set_filter_by(self, filter_by):
        self.filter_by.click()
        xpath = '//div[contains(@class, "option-ex-text") and text()="{0}"]'.format(filter_by)
        self._web_driver.find_element_by_xpath(xpath).click()

    def set_filter_method(self, filter_method):
        self.filter_method.click()
        xpath = '//div[contains(@class, "option-ex-text") and text()="{0}"]'.format(filter_method)
        self._web_driver.find_element_by_xpath(xpath).click()

    def configure_advanced_filter(self, filter_id, params):
        default_options = ['Include', 'Ad', 'Text Contains']

        for i, value in enumerate(params):
            xpath = ('(//div[contains(@class, "item__layout")])[{0}]'
                     '//div[text()="{1}"]').format(filter_id, default_options[i])
            xpath_element = ('//div[contains(@class, "option-ex-text")'
                             'and text()="{0}"]').format(value)
            self._web_driver.find_element_by_xpath(xpath).click()
            self._web_driver.find_element_by_xpath(xpath_element).click()

    def set_page_size(self, page_size=10):
        xpath_pattern = ('//div[text()="{0}" and (contains(@class, "option")'
                         'or contains(@class, "select"))]')
        self._web_driver.find_element_by_xpath(xpath_pattern.format('10')).click()
        self._web_driver.find_element_by_xpath(xpath_pattern.format(page_size)).click()

        self.wait_page_loaded()

class MPages(WebPage):
    melements = WebElement(xpath='//div[contains(@class, "shown")]//span[contains(text(), "Отчеты по исполнительской дисциплине")]')
    m2elements = WebElement(xpath='//a[contains(text(), "Состояние исполнения резолюций")]')

    # Форма авторизации
    username_text = WebElement(name=KSEDLocators.username_text) # Логин
    password_text = WebElement(name=KSEDLocators.password_text) # Пароль
    LogIn_button = WebElement(xpath=KSEDLocators.LogIn_button) # Кнопка "Войти"


    # *******СТРОКА МЕНЮ*******
    ksed = WebElement(xpath=KSEDLocators.ksed) #xpath  # КСЭД

    barcode_search = WebElement(id_=KSEDLocators.barcode_search) #id  # Поиск по ШК
    search_bc = WebElement(xpath=KSEDLocators.search_bc) # Строка поиска по ШК

    more_menu = WebElement(id_=KSEDLocators.more_menu)# Меню "Ещё"
    ksed_in_more_m = WebElement(id_=KSEDLocators.ksed_in_more_m) # КСЭД в меню "Ещё"
    Company_dir = WebElement(xpath=KSEDLocators.Company_dir)  # Справочник организации
    admin = WebElement(xpath=KSEDLocators.admin) # Администрирование
    transfer = WebElement(xpath=KSEDLocators.transfer) # Передача дел
    arm_arh = WebElement(xpath=KSEDLocators.arm_arh) # АРМ Архивное дело
    verify = WebElement(xpath=KSEDLocators.verify) # Верификация
    scanner = WebElement(xpath=KSEDLocators.scanner) # Работа со сканером ШК

    notification = WebElement(id_=KSEDLocators.notification) # Уведомления
    notificationProtokol = WebElement(xpath=KSEDLocators.notificationProtokol) # Первое в списке уведомление о протоколе
    notificationFirst = WebElement(xpath=KSEDLocators.notificationFirst)  # id  # Уведомление первое в списке
    # *******МЕНЮ ПОЛЬЗОВАТЕЛЯ*******
    user_menu = WebElement(id_=KSEDLocators.user_menu) # Меню пользователя
    USER_LOGOUT = WebElement(id_=KSEDLocators.USER_LOGOUT) # Выход из системы

    my_profile = WebElement(xpath=KSEDLocators.my_profile) # Пункт меню "Мой профиль"
    fieldlabel = WebElement(xpath=KSEDLocators.fieldlabel) # Должность в области краткой информации
    btnEdit_profile = WebElement(xpath=KSEDLocators.btnEdit_profile) # Кнопка "Изменить профиль"
    inputPosition = WebElement(xpath=KSEDLocators.inputPosition) # Поле ввода должности

    logic_ESM = WebElement(xpath=KSEDLocators.logic_ESM) # Пункт меню "Логика ECM. Мой профиль"
    autoAnswerText = WebElement(name=KSEDLocators.autoAnswerText) # Текст автоответа (Меня нет в офисе)
    btnCancelAbsence = WebElement(xpath=KSEDLocators.btnCancelAbsence) # Кнопка "Отменить отсутствие"
    btnYes = WebElement(xpath=KSEDLocators.btnYes) # Кнопка "Да" (отменить отсутствие)

    edit_password = WebElement(xpath=KSEDLocators.edit_password) # Пункт меню "Изменить пароль"
    inputOldPassword = WebElement(xpath=KSEDLocators.inputOldPassword) # Введите старый пароль
    inputNewPassword1 = WebElement(xpath=KSEDLocators.inputNewPassword1) # Введите старый пароль
    inputNewPassword2 = WebElement(xpath=KSEDLocators.inputNewPassword2) # Введите старый пароль
    btnOKchange = WebElement(xpath=KSEDLocators.btnOKchange) # Кнопка "Изменить пароль"

    # *******ЛЕВАЯ ЧАСТЬ СТРАНИЦЫ (Кнопка "Создать" и разделы)*******
    newDoc_button = WebElement(xpath=KSEDLocators.newDoc_button) # "Создать"

    protocol = WebElement(xpath=KSEDLocators.protocol) # Протокол
    rd = WebElement(xpath=KSEDLocators.rd) # РД
    reestr = WebElement(xpath=KSEDLocators.reestr) # Реестр
    poruchenie = WebElement(xpath=KSEDLocators.poruchenie) # Поручение
    resolution = WebElement(xpath=KSEDLocators.resolution) # Резолюция
    SZ = WebElement(xpath=KSEDLocators.SZ) # Служебная записка
    proizvDoc = WebElement(xpath=KSEDLocators.proizvDoc) # Произвольный документ
    paket_vh = WebElement(xpath=KSEDLocators.paket_vh) #Пакет Вх. кор.
    vhDoc = WebElement(xpath=KSEDLocators.vhDoc) # Входящий документ
    ishDoc = WebElement(xpath=KSEDLocators.ishDoc) # Исходящий документ

    # РАЗДЕЛЫ
    myWork = WebElement(xpath=KSEDLocators.myWork) # Моя работа

    expedition = WebElement(xpath=KSEDLocators.expedition) # Экспедиция

    navigation = WebElement(xpath=KSEDLocators.navigation) # Навигатор

    allur = WebElement(xpath=KSEDLocators.allur) # Отчеты

    workReg = WebElement(xpath=KSEDLocators.workReg) # Работа регистратора

    medo = WebElement(xpath=KSEDLocators.medo) # МЭДО

    mySearch = WebElement(xpath=KSEDLocators.mySearch) # Мои поисковые запросы
    poiskzapr = WebElement(xpath=KSEDLocators.poiskzapr) # Поисковые запросы
    myPoiskZapr = WebElement(xpath=KSEDLocators.myPoiskZapr) # Поисковые запросы
    ControlZapr = WebElement(xpath=KSEDLocators.ControlZapr) # Упарвление поисковыми запросами
    # ОБЛАСТЬ ПРОСМОТРА (КСЭД)
    oblProsm = WebElement(xpath=KSEDLocators.oblProsm) # Область просмотра
    oneDocInList = WebElement(xpath=KSEDLocators.oneDocInList) # Первый документ в списке
    nineDocInList = WebElement(xpath=KSEDLocators.nineDocInList) # Девятый документ в списке
 ###################   subordinate = MultiWebElement(xpath=KSEDLocators.subordinate) # "+" раскрытие подчиненные документы
    oneSubordInList = WebElement(xpath=KSEDLocators.oneSubordInList) # Первая ссылка на подчиненный документ
    ActionTab = WebElement(xpath=KSEDLocators.ActionTab) # Кнопка "Действия с выбранными"
    chBinOnl = WebElement(xpath=KSEDLocators.chBinOnl)

    # Моя работа
    WorkImmid = WebElement(xpath=KSEDLocators.WorkImmid)  # xpath  # Моя работа - срочные
    connectedDoc = WebElement(xpath=KSEDLocators.connectedDoc) # xpath #  связанные документы

    # ОТЧЕТЫ
    section_allur = WebElement(xpath=KSEDLocators.section_allur) # Раздел "Отчеты"
    node_Logs = WebElement(xpath=KSEDLocators.node_Logs)  # "Журналы"

    node_Statis = WebElement(xpath=KSEDLocators.node_Statis) # "Статистические отчеты"
    edsBykindStat = WebElement(xpath=KSEDLocators.edsBykindStat) # Отчет "Сводка по видам документов"

    node_ispDisp = WebElement(xpath=KSEDLocators.node_ispDisp) #

    logs_incDoc = WebElement(xpath=KSEDLocators.logs_incDoc)
    incomingRegJournal = WebElement(xpath=KSEDLocators.incomingRegJournal) # Отчет "Журнал регистрации входящих документов"
    logs_outDoc = WebElement(xpath=KSEDLocators.logs_outDoc)
    outgoingRegistration = WebElement(xpath=KSEDLocators.outgoingRegistration) # Отчет "Журнал регистрации исходящих документов"
    logs_raspDoc = WebElement(xpath=KSEDLocators.logs_raspDoc)
    ordRegJournal = WebElement(xpath=KSEDLocators.ordRegJournal) # Отчет "Журнал регистрации Распорядительных документов"
    logs_sluDoc = WebElement(xpath=KSEDLocators.logs_sluDoc)
    internalRegJournal = WebElement(xpath=KSEDLocators.internalRegJournal) # Отчет "Журнал регистрации служебных записок"

    stat_specDoc = WebElement(xpath=KSEDLocators.stat_specDoc)
    stat_temDoc = WebElement(xpath=KSEDLocators.stat_temDoc)
    edsBySubjectStat = WebElement(xpath=KSEDLocators.edsBySubjectStat) # Отчет "Сводка по тематикам документов"
    stat_temDocO = WebElement(xpath=KSEDLocators.stat_temDocO)
    edsBySubjectStatO = WebElement(xpath=KSEDLocators.edsBySubjectStatO) # Отчет "Сводка по тематикам документов(объед)"
    stat_tipDoc = WebElement(xpath=KSEDLocators.stat_tipDoc)
    edByTypeStat = WebElement(xpath=KSEDLocators.edByTypeStat) # Отчет "Сводка по типам документов"

    allu_ispIncDoc = WebElement(xpath=KSEDLocators.allu_ispIncDoc)
    allu_raspDoc = WebElement(xpath=KSEDLocators.allu_raspDoc)
    allu_sluDoc = WebElement(xpath=KSEDLocators.allu_sluDoc)
    allu_ispDis = WebElement(xpath=KSEDLocators.allu_ispDis)
    allu_ispDispA = WebElement(xpath=KSEDLocators.allu_ispDispA)
    allu_NispDI = WebElement(xpath=KSEDLocators.allu_NispDI)
    allu_NispDIrg = WebElement(xpath=KSEDLocators.allu_NispDIrg)
    allu_istS = WebElement(xpath=KSEDLocators.allu_istS)
    allu_narS = WebElement(xpath=KSEDLocators.allu_narS)
    allu_prodIsp = WebElement(xpath=KSEDLocators.allu_prodIsp)
    allu_prodPodr = WebElement(xpath=KSEDLocators.allu_prodPodr)
    allu_ReesContr = WebElement(xpath=KSEDLocators.allu_ReesContr)
    allu_ReesContrN = WebElement(xpath=KSEDLocators.allu_ReesContrN)
    allu_ReesContrF = WebElement(xpath=KSEDLocators.allu_ReesContrF)
    allu_SostIspR = WebElement(xpath=KSEDLocators.allu_SostIspR)


    # *******РАБОТА С ДОКУМЕНТАМИ*******

    # ОБЩИЕ АТРИБУТЫ
    #(форма создания документа)
    title = WebElement(name=KSEDLocators.title)  # Заголовок

    category_doc = WebElement(xpath=KSEDLocators.category_doc) # Категория документа

    doc_type = WebElement(xpath=KSEDLocators.doc_type) # Вид документа(кнопка выбора)
    doc_typeInp = WebElement(xpath=KSEDLocators.doc_typeInp) # Вид документа(поле ввода)
    btnOKDT = WebElement(xpath=KSEDLocators.btnOKDT) # Вид документа (кнопка "ОК")

    podpisant = WebElement(xpath=KSEDLocators.podpisant) # Подписант(ы)

    sposob_dost = WebElement(xpath=KSEDLocators.sposob_dost) # Способ доставки

    btnCreateDoc = WebElement(xpath=KSEDLocators.btnCreateDoc) # Кнопка "Создать"

    adresat = WebElement(xpath=KSEDLocators.adresat) # Адресат

    korrespondent = WebElement(xpath=KSEDLocators.korrespondent)  # Корреспондент

    # (карточка документа)
    attachments = WebElement(xpath=KSEDLocators.attachments) # # Переход во вкладку "Вложения"
    vlozheniya = WebElement(xpath=KSEDLocators.vlozheniya) # Вложения (раскрытие раздела)
    osnSvedeniya = WebElement(xpath=KSEDLocators.osnSvedeniya) # Основные сведения (раскрытие раздела)
    printForm = WebElement(xpath=KSEDLocators.printForm)# Печатные формы (раскрытие раздела)
    printBarCode = WebElement(xpath=KSEDLocators.printBarCode) #Печатная форма штрих кода документа
    btnPrintInPrintForm = WebElement(id_=KSEDLocators.btnPrintInPrintForm)# Кнопка печати в окне печатной формы
    btnOKpodpis = WebElement(xpath=KSEDLocators.btnOKpodpis) # Кнопка ОК подтверждение подписания

    mode = WebElement(xpath=KSEDLocators.mode) # Переключение в двупанельный вид
    fileUpload = WebElement(xpath=KSEDLocators.fileUpload) # Загрузить файл
    fileUpload2 = WebElement(xpath=KSEDLocators.fileUpload2)  # Загрузить файл в поручении
    files = WebElement(xpath=KSEDLocators.files) # Выберите файлы
    show = WebElement(xpath=KSEDLocators.show) # Показать общую карточка
    show_list = WebElement(xpath=KSEDLocators.show_list)# Показать ввиде списка
    btnPrint = WebElement(xpath=KSEDLocators.btnPrint) # Кнопка печати в форме предварительного просмотра вложения

    soglasovanieWkladka = WebElement(xpath=KSEDLocators.soglasovanieWkladka) # Вкладка "Согласование"
    createRuleBtn = WebElement(xpath=KSEDLocators.createRuleBtn) # Кнопка "Создать маршрут"
    createRuleIndivid = WebElement(xpath=KSEDLocators.createRuleIndivid) # "Индивидуальный маршрут"
    addEtap = WebElement(xpath=KSEDLocators.addEtap) # Кнопка "Добавить этап"
    tipeEtap = WebElement(xpath=KSEDLocators.tipeEtap) # "Вид этапа"
    soglasuychie = WebElement(xpath=KSEDLocators.soglasuychie) # "Согласующие"
    btnOKformSogl = WebElement(xpath=KSEDLocators.btnOKformSogl) # Кнопка "ОК" на форме добавления этапа согласования

    punkti = WebElement(xpath=KSEDLocators.punkti) # Вкладка "Пункты"
    punktiBtn = WebElement(xpath=KSEDLocators.punktiBtn) # Кнопка "Пункты"
    punktPoruch = WebElement(xpath=KSEDLocators.punktPoruch) # Пункт/Поручение
    textPoruch = WebElement(xpath=KSEDLocators.textPoruch) # Текст поручения
    tipPoruch = WebElement(xpath=KSEDLocators.tipPoruch) # Тип поручения
    otvetstv_ispolnVpunktah = WebElement(xpath=KSEDLocators.otvetstv_ispolnVpunktah) # Ответственный исполнитель в пунктах карточки документа
    srokIspoln = WebElement(xpath=KSEDLocators.srokIspoln) # Срок исполнения (среднее знач)

    btnOKform = WebElement(xpath=KSEDLocators.btnOKform) # Кнопка ОК на форме

    sendFor_approval = WebElement(xpath=KSEDLocators.sendFor_approval) # Действие "Направить на согласование"
    sendFor_podpis = WebElement(xpath=KSEDLocators.sendFor_podpis) # Действие "Направить на подписание"
    sendFor_execution = WebElement(xpath=KSEDLocators.sendFor_execution) # Действие "Направить на исполнение"
    btnOKnaprNaIspoln = WebElement(xpath=KSEDLocators.btnOKnaprNaIspoln) # Кнопка "ОК" на форме подтверждения действия "Направить на исполнение"
    confirm = WebElement(xpath=KSEDLocators.confirm) # Подтверждение согласования
    confirm2 = WebElement(xpath=KSEDLocators.confirm2)  # Подтверждение согласования
    confirm_3 = WebElement(xpath=KSEDLocators.confirm_3)  # Подтверждение согласования

    status_Doc = WebElement(xpath=KSEDLocators.status_Doc) # Статус документа во вкладке (Основные сведения)

    #"Отправить отчет"
    actionSendAllere = WebElement(xpath=KSEDLocators.actionSendAllere) # "Отправить отчет" действие
    btnSend = WebElement(xpath=KSEDLocators.btnSend) # Кнопка "Отправить"
    textAllur = WebElement(xpath=KSEDLocators.textAllur) # Текстовое поле "Текст отчета"
    btnAddSvyz = WebElement(xpath=KSEDLocators.btnAddSvyz) # Кнопка добавления связи "..."
    searchDoc = WebElement(xpath=KSEDLocators.searchDoc) # Строка поиска в форме подбора
    oneListEl = WebElement(xpath=KSEDLocators.oneListEl) # Первый элемент в списке справочника
    btnOK = WebElement(xpath=KSEDLocators.btnOK) # Кнопка "ОК" в форме подбора

    # (панель согласования)
    APPROVED_button = WebElement(xpath=KSEDLocators.APPROVED_button) # Кнопка "Согласовать"
    APPROVED_WITH_REMARK_button = WebElement(xpath=KSEDLocators.APPROVED_WITH_REMARK_button) # Кнопка "Согласовать с комментариями"
    REJECTED_button = WebElement(xpath=KSEDLocators.REJECTED_button) # Кнопка "Отклонить"
    internal_approval = WebElement(xpath=KSEDLocators.internal_approval) # Кнопка "Внутреннее согласование"
    prop_bpm_comment = WebElement(name=KSEDLocators.prop_bpm_comment) # Поле комментария
    apply_button_button = WebElement(xpath=KSEDLocators.apply_button_button) # Кнопка "ОК" при вынесении решения согласования

    SIGNED_button = WebElement(xpath=KSEDLocators.SIGNED_button) # Кнопка "Подписать"

    # # ПРОТОКОЛ
    # #(форма создания документа)
    # addEl = WebElement(xpath=KSEDLocators.addEl) # Вид документа(Протокол совещания рабочей группы)
    # addEl2 = WebElement(xpath=KSEDLocators.addEl2) #Вид документа "Служебная записка"

    # РАСПОРЯДИТЕЛЬНЫЙ ДОКУМЕНТ
    #(форма создания документа)
    addEl = WebElement(xpath=KSEDLocators.addEl) # Вид документа(Протокол совещания рабочей группы)
    addEl2 = WebElement(xpath=KSEDLocators.addEl2) #Вид документа "Служебная записка"
    preambula = WebElement(xpath=KSEDLocators.preambula) # Преамбула
    obcontrol = WebElement(xpath=KSEDLocators.obcontrol) # Общий контроль
    wid_doc = WebElement(xpath=KSEDLocators.wid_doc) # Вид документа (в РД)
    wid_doc_rasp = WebElement(xpath=KSEDLocators.wid_doc_rasp) # Вид документа РД (Распоряжение)

    addPunkt = WebElement(xpath=KSEDLocators.addPunkt) # Кнопка "Добавить пункт"
    textPunktaRD = WebElement(name=KSEDLocators.textPunktaRD) # Текст пункта РД
    otvetstv_ispolnVpunktahRD = WebElement(xpath=KSEDLocators.otvetstv_ispolnVpunktahRD) # Ответственный исполнитель в пункте РД
    rassilka = WebElement(xpath=KSEDLocators.rassilka) # Вкладка "Рассылка"
    btnVipolnit = WebElement(xpath=KSEDLocators.btnVipolnit) # Кнопка "Выполнить..."
    punktBtnVipolnit = WebElement(xpath=KSEDLocators.punktBtnVipolnit) # Создать и заполнить


    # ПРОТОКОЛ
    #(форма создания документа)
    date = WebElement(xpath=KSEDLocators.date) # Дата совещания
    category = WebElement(xpath=KSEDLocators.category) # Категория
    Chairman = WebElement(xpath=KSEDLocators.Chairman) # Председатель
    Secretary = WebElement(xpath=KSEDLocators.Secretary) # Секретарь
    person_present = WebElement(xpath=KSEDLocators.person_present) # Присутствовали


    #РЕЕСТР
    #(форма создания документа)
    vid_reestra = WebElement(xpath=KSEDLocators.vid_reestra) # Вид реестра
    vid_reestraPR = WebElement(xpath=KSEDLocators.vid_reestraPR) # Вид реестра (Передачи на рег..)
    vid_reestraPP = WebElement(xpath=KSEDLocators.vid_reestraPP) # Вид реестра (Приема/передачи)
    btnCreateChern = WebElement(xpath=KSEDLocators.btnCreateChern)  # Кнопка "Создать черновик"
    btnCreateSend = WebElement(xpath=KSEDLocators.btnCreateSend) # Кнопка "Создать и отправить"
    inpDoc = WebElement(xpath=KSEDLocators.inpDoc) # Поле "Документы"
    poluchatel = WebElement(xpath=KSEDLocators.poluchatel) # Поле "Получатель"

    # СЛУЖЕБНАЯ ЗАПИСКА
    #(форма создания документа)
    adresati = WebElement(xpath=KSEDLocators.adresati) # Адресаты

    # ПРОИЗВОЛЬНЫЙ ДОКУМЕНТ
    #(форма создания документа)
    prorabotka = WebElement(xpath=KSEDLocators.prorabotka) # Проработка
    chBprorab = WebElement(xpath=KSEDLocators.chBprorab) # чекбокс проработка
    normokontrol = WebElement(xpath=KSEDLocators.normokontrol) # Нормоконтроль
    chBnorm = WebElement(xpath=KSEDLocators.chBnorm) # чекбокс Проработка
    soglasovanie = WebElement(xpath=KSEDLocators.soglasovanie) # Согласование
    podpisanie = WebElement(xpath=KSEDLocators.podpisanie) # Подписание
    utverzhdenie = WebElement(xpath=KSEDLocators.utverzhdenie) # Утверждение
    oznakomlenie = WebElement(xpath=KSEDLocators.oznakomlenie) # Ознакомление

    # ПОРУЧЕНИЕ
    # (форма создания документа)
    tipPoruch = WebElement(xpath=KSEDLocators.tipPoruch) # Тип поручения
    text_poruch = WebElement(name=KSEDLocators.text_poruch) #Текст поручения
    otvetstv_ispoln = WebElement(xpath=KSEDLocators.otvetstv_ispoln) # Ответственный исполнитель

    # ПАКЕТ ВХОДЯЩЕЙ КОРРЕСПОНДЕНЦИИ

    # ВХОДЯЩИЙ ДОКУМЕНТ
    #(форма создания документа)
    ishNumber = WebElement(name=KSEDLocators.ishNumber) # Исходящий номер
    dateIS = WebElement(xpath=KSEDLocators.dateIS) # Дата исходящего

    # ИСХОДЯЩИЙ ДОКУМЕНТ
    # (форма создания документа)
    osnovPodpis = WebElement(name=KSEDLocators.osnovPodpis) # Основание подписания
    korrespondentISH = WebElement(xpath=KSEDLocators.korrespondentISH) # Корреспондент


    clickNull = WebElement(xpath=KSEDLocators.clickNull) # КЛИК ВНЕ АТРИБУТОВ


    #Формы отчетов

    #Мои поисковые запросы
    listChange = WebElement(xpath=KSEDLocators.listChange)  # Выпадающий список
    listChangeSZ = WebElement(xpath=KSEDLocators.listChangeSZ)  # Выпадающий список - служебная записка
    listChangeRD = WebElement(xpath=KSEDLocators.listChangeRD)  # Выпадающий список - РД
    butSave = WebElement(xpath=KSEDLocators.butSave) #Кнопка сохранить
    nameZap = WebElement(xpath=KSEDLocators.nameZap) #Наименование запроса
    zaprosToDel = WebElement(xpath=KSEDLocators.zaprosToDel)#созданный запрос
    butDel = WebElement(xpath=KSEDLocators.butDel) #Кнопка удалить
    butRed = WebElement(xpath=KSEDLocators.butRed)  # Кнопка редактировать
    butDelAc = WebElement(xpath=KSEDLocators.butDelAc)  # Кнопка удалить подтверждение
    butAct = WebElement(xpath=KSEDLocators.butAct) # Кнопка "Действия с выбранными"
    butAct_2 = WebElement(xpath=KSEDLocators.butAct_2)  # Кнопка "Действия с выбранными"
    butExp = WebElement(xpath=KSEDLocators.butExp)  # Кнопка экспорта
    butExp_2 = WebElement(xpath=KSEDLocators.butExp_2)  # Кнопка экспорта
    checkBoxFirst = WebElement(xpath=KSEDLocators.checkBoxFirst)  # Первый чекбокс в списке
    butFavorite = WebElement(xpath=KSEDLocators.butFavorite)  # Кнопка добавить в избранное
    butOK = WebElement(xpath=KSEDLocators.butOK) #Кнопка OK добавить в избранное
    butSelExp = WebElement(xpath=KSEDLocators.butSelExp)  # Кнопка экспорта выбранного