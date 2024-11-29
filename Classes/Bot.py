import time
import winsound
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Bot:
    """
    Класс, отвечающий за работу бота в рамках сайта Берёзка
    """
    def login_by_signature(self, driver):
        """
        Входит на сайт по электронной цифровой подписи (ЭЦП).
        :param self: Параметр бота.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            selector = ".btn-block.mb-3"  # ".btn-block.mb-0" для госуслуг

            if driver.find_elements(By.CSS_SELECTOR, selector):
                driver.find_elements(By.CSS_SELECTOR, selector)[0].click()
                break
            else:
                time.sleep(1)

    def fill_inn_field(self, driver, inn):
        """
        Автоматически заполняет поле ввода ИНН на веб-странице.
        :param self: Параметр бота.
        :param driver: Объект WebDriver, который управляет браузером.
        :param inn: Строка, содержащая ИНН, который необходимо ввести в поле.
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_elements(By.CSS_SELECTOR, "#filterField-14-autocomplete"):
                text_field1 = driver.find_elements(By.CSS_SELECTOR, "#filterField-14-autocomplete")[0]
                text_field1.send_keys(inn)
                break
            else:
                time.sleep(1)

    def init_options(self):
        """
        Инициализирует конфигурации для веб-драйвера Selenium.
        :param self: Параметр бота.
        :return: Возвращает настроенный объект Options, который может быть использован при создании экземпляра
        веб-драйвера.
        """
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory=Default')
        options.add_extension(r'./CryptoPro-Extension-for-CAdES-Browser-Plug-in-Chrome.crx')

        # Дополнительные параметры для повышения производительности
        options.add_argument("--disable-software-rasterizer")  # Отключение программного рендеринга
        options.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm
        options.add_argument("--disable-logging")  # Отключение логирования
        options.add_argument("--disable-features=VizDisplayCompositor")  # Отключение визуальных фич

        options.add_argument("--disable-plugins")  # Отключает все плагины в браузере

        # Отключение всех расширений, которые явно добавлены с помощью --load-extension # noqa
        options.add_argument("--disable-extensions")

        options.page_load_strategy = 'normal'

        return options

    def choice_inn_popup(self, driver, inn):
        """
        Выбирает всплывающий элемент с указанным ИНН.
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param inn: Строка, содержащая ИНН, который нужно найти на странице.
        :return: Ничего не возвращает.
        """
        while True:
            try:
                element = driver.find_element(
                    By.XPATH,
                    "//span[contains(text(), "
                    f"'ИНН: {inn}')]"
                )
                element.click()
                break
            except NoSuchElementException:
                print("Элемент с текстом ИНН не найден, пробуем ещё раз...")
                time.sleep(5)

    def fill_search_text_field(self, driver, search_text):
        """
        Заполняет поля поиска на веб-странице с указанным словом.
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            try:
                element = driver.find_element(By.ID, "searchText")
                element.send_keys(search_text)
                break
            except NoSuchElementException:
                print("Элемент #searchText не найден, пробуем ещё раз...")
                time.sleep(5)

    def monitor_element_presence(self, driver, css_selector):
        """
        Мониторит наличие элемента на веб-странице по CSS-селектору.
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param css_selector: Строка, содержащая CSS-селектор элемента, который нужно отслеживать.
        :return: Ничего не возвращает.
        """
        if driver.find_elements(By.CSS_SELECTOR, css_selector):
            while True:
                if driver.find_elements(By.CSS_SELECTOR, css_selector):
                    print(f"{css_selector} найден")
                    time.sleep(1)
                else:
                    print(f"{css_selector} не найден")
                    break

    def login_by_gosuslugi(self, driver):
        """
        Выполняет полный вход через госуслуги.
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        if driver.find_elements(By.CSS_SELECTOR, ".plain-button_light"):
            while True:
                if driver.find_elements(By.CSS_SELECTOR, ".plain-button_light"):
                    self.full_login(driver)
                    break
                else:
                    time.sleep(1)

    def wait_for_element_and_click(self, driver, css_selector):
        """
        Ожидает наличие указанного элемента и кликает на него, если находит
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param css_selector: селектор, который необходимо найти
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_elements(By.CSS_SELECTOR, css_selector):
                autocomp = driver.find_elements(By.CSS_SELECTOR, css_selector)[0]
                print(f"{css_selector} найден", autocomp)
                autocomp.click()
                break
            else:
                print(f"{css_selector} не найден")
                time.sleep(1)

    def click_by_search(self, driver, sleep_time):
        """
        Кликает по кнопке Показать
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param sleep_time: Время задержки.
        :return: Возвращает элемент с кнопкой Показать.
        """
        refresh_btn = driver.find_element(By.ID, "applyFilterButton")
        refresh_btn.click()
        time.sleep(sleep_time)
        return refresh_btn

    def action_with_lots_or_refresh(self, driver, refresh_btn):
        """
        Читает номер лота из lot_numbers.txt, если его нет - добавляет в файл и подаёт заявку,
        если есть - удаляет карточку лота. Если не находится лот, то нажимает кнопку Показать
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param refresh_btn: Кнопка перезагрузить.
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_elements(By.ID, "tradeNumber"):
                lotNum = driver.find_element(By.ID, "tradeNumber").get_attribute("innerText")
                with open('../lot_numbers.txt', 'r') as r:
                    if lotNum in r.read():
                        driver.execute_script("document.getElementsByClassName('card')[0].remove()")
                    else:
                        with open('../lot_numbers.txt', 'a') as f:
                            f.write(lotNum)
                            if driver.find_element(By.ID, "applicationSendButton"):
                                winsound.Beep(1000, 1000)
                                driver.find_element(By.ID, "applicationSendButton").click()
                            break
            else:
                refresh_btn.click()
                time.sleep(2)

    def add_documents_from_repository(self, driver):
        """
        Кликает по кнопке Добавить из хранилища, после чего добавляет первый отображаемый документ и вписывает
        в поле Наименование слово Документы
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        if driver.find_elements(By.CSS_SELECTOR, ".load-from-storage-btn"):
            loadDoc = driver.find_elements(By.CSS_SELECTOR, ".load-from-storage-btn")[0]
            loadDoc.click()
            while True:
                if driver.find_elements(By.CSS_SELECTOR, ".add-document-btn"):
                    addDoc = driver.find_elements(By.CSS_SELECTOR, ".add-document-btn")[0]
                    addDoc.click()
                    docName = driver.find_element(By.ID, "documentEditableNameInput-0")
                    docName.send_keys('Документы')
                    break
                else:
                    time.sleep(1)

    def remove_date_end_application(self, driver):
        """
        Зачем-то удаляет дату окончания предложения, если она есть. Метод под вопросом
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_elements(By.CLASS_NAME, "fixed-filling"):
                driver.execute_script("document.getElementsByClassName('fixed-filling')[0].remove()")
                break
            else:
                time.sleep(1)

    def set_price(self, driver, base_price):
        """
        Устанавливает цены первого элемента (Сперва стирает установленную по умолчанию цену)
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param base_price: Базовая цена подачи цены за единицу услуги (товара)
        :return: Ничего не возвращает.
        """
        price_field = driver.find_element(By.ID, "lotItemPriceInput-0")

        for _ in range(20):
            price_field.send_keys(Keys.BACKSPACE)

        if "." in base_price:
            price_field.send_keys(base_price.replace(".", ","))
        else:
            price_field.send_keys(base_price)

    def click_on_value_added_tax(self, driver):
        """
        Кликает на Не облагается в колонке Задать для всех позиций НДС.
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_elements(By.CSS_SELECTOR, ".tax"):
                driver.find_elements(By.CSS_SELECTOR, ".tax")[0].click()
                break
            else:
                time.sleep(1)

    def click_by_element_from_elements(self, driver, element, order):
        """
        Кликает на элемент в коллекции элементов с одинаковым названием
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :param element: Элемент, на который нужно кликнуть.
        :param order: Порядковый номер элемента в коллекции элементов с одним и тем же названием.
        :return: Ничего не возвращает.
        """
        if driver.find_elements(By.CLASS_NAME, element):
            buttons = driver.find_elements(By.CLASS_NAME, element)
            buttons[order].click()

    def click_on_add_offer(self, driver):
        """
        Кликает на элемент с id add-offer (вероятнее всего предложение) (ЭЦП не с собой, как будет у меня точно укажу)
        :param self: Параметр бота.
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            if driver.find_element(By.ID, "add-offer"):
                truBtn = driver.find_element(By.ID, "add-offer")
                truBtn.click()
                time.sleep(1)
                break
            else:
                time.sleep(1)

    def full_login(self, driver):
        """
        Кликает по кнопкам, через которые можно войти в аккаунт с помощью госуслуг.
        :param self: Параметр бота
        :param driver: Объект веб-драйвера Selenium, который используется для взаимодействия с веб-страницей.
        :return: Ничего не возвращает.
        """
        while True:
            elements = driver.find_elements(By.CSS_SELECTOR, ".plain-button_light")

            if elements and elements[1].get_attribute("innerText") == "Эл. подпись":
                driver.find_elements(By.CSS_SELECTOR, ".plain-button_light")[1].click()
                while True:
                    if driver.find_elements(By.CSS_SELECTOR, ".plain-button_wide"):
                        driver.find_elements(By.CSS_SELECTOR, ".plain-button_wide")[0].click()
                        break
                    else:
                        time.sleep(1)
            elif "gosuslugi" not in driver.current_url:
                if driver.find_elements(By.CSS_SELECTOR, "#orglist"):
                    while True:
                        if driver.find_elements(By.CSS_SELECTOR, "#orglist"):
                            time.sleep(1)
                        else:
                            break
                break
            else:
                time.sleep(1)
