import json
import requests
import time
import winsound

from Objects.search import search_model
from Objects.headers import get_headers
from Objects.document_request import document_request_model
from Objects.tax_request import get_tax
from Objects.sign_request_model import get_sign


class RequestBot:
    """Класс, отвечающий за работу бота, подающего предложения через запросы, а не через интерфейс."""

    def get_cookies(self, driver):
        """
        Получает куки.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Объект с куки
        """
        cookies = list(driver.get_cookies())
        cookie_objects = []

        for cookie in cookies:
            cookie_object = {
                "Name": cookie["name"],
                "Value": cookie["value"]
            }
            cookie_objects.append(cookie_object)

        return cookie_objects

    def get_local_storage(self, driver):
        """
        Получить значения из локального хранилища.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Объект со значениями локального хранилища.
        """
        script = """
                var items = {};
                for (var i = 0; i < localStorage.length; i++){
                    var key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
                """
        local_storage_items = driver.execute_script(script)

        return local_storage_items

    def get_access_token(self, local_storage_items):
        """
        Получает токен доступа.
        :param local_storage_items: Объект со всеми значениями локального хранилища.
        :return: Токен доступа.
        """
        authorization_data = local_storage_items['0-eat_ui']
        authorization_data_dict = json.loads(authorization_data)
        authn_result = authorization_data_dict['authnResult']
        token_access = authn_result['access_token']

        return token_access

    def get_cart_id(self, local_storage_items):
        """
        Получение id карточки лота
        :param local_storage_items: Объект со всеми значениями локального хранилища.
        :return: Токен доступа.
        """
        cart_id = local_storage_items['cart_id']

        return cart_id

    def send_get_request(self, session, url, access_token):
        """
        Отправляет get-запрос.
        :param session: Сессия requests.
        :param url: Адрес запроса.
        :param access_token: Токен доступа.
        :return: Ответ на запрос или None
        """
        headers = get_headers(access_token)

        start_time = time.time()

        response = session.get(url, headers=headers)

        end_time = time.time()

        print(f"GET запрос к {url} занял {end_time - start_time:.2f} секунд")

        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                print("Ошибка: ответ не является валидным JSON")
                print(response.text)
                return None
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None

    def send_post_request(self, session, url, access_token, request_model=None, cookie=None):
        """
        Отправляет post-запрос.
        :param session: Сессия requests.
        :param url: Адрес запроса.
        :param access_token: Токен доступа.
        :param request_model: Модель запроса, передаваемая в параметры.
        :return: Ответ на запрос или None
        """
        headers = get_headers(access_token)

        start_time = time.time()

        response = session.post(url, headers=headers, json=request_model)

        end_time = time.time()

        print(f"POST запрос к {url} занял {end_time - start_time:.2f} секунд")

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None

    def find_lots(self, session, access_token):
        """
        Отправка текста поиска лотов.
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными, найденных лотов.
        """
        url = "https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots"

        lots_data = self.send_post_request(session, url, access_token, search_model)

        return lots_data

    def send_application(self):
        print("Подача предложения")
        # TODO сделать реализацию подачи заявки

    def find_documents_from_repository(self, session, access_token, cookies=None):
        """
        Находит документы из хранилища.
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными найденных документов.
        """
        url = "https://registry-api.agregatoreat.ru/api/OrganizationDocuments/get-list"

        documents_data = self.send_post_request(session=session, url=url, access_token=access_token,
                                                request_model=document_request_model, cookie=cookies)

        return documents_data

    def get_cart_lot(self, session, lot_id, access_token):
        """
        Получение данных о лоте (получение карточки лота)
        :param session: Сессия requests.
        :param lot_id: GUID для искомого лота.
        :param access_token: Токен доступа.
        :return: Объект с данными лота.
        """
        url = f"https://tender-api.agregatoreat.ru/api/Application/new/{lot_id}"

        cart_lot = self.send_get_request(session, url, access_token)

        return cart_lot

    def set_not_taxed(self, session, access_token, price):
        """
        Устанавливает налог на Не облагается
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :param price: Цена, на которую устанавливается налог
        :return: Объект с данными ответа.
        """
        url = "https://tender-api.agregatoreat.ru/api/TaxCalculation"
        tax_request_model = get_tax(price)

        tax_response = self.send_post_request(session=session, url=url, access_token=access_token, request_model=tax_request_model)

        return tax_response

    def get_sign_info(self, session, access_token):
        """
        Получает информацию о подписи
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными подписи
        """
        url = "https://registry-api.agregatoreat.ru/api/User/self"

        sign_info_response = self.send_get_request(session=session, url=url, access_token=access_token)

        return sign_info_response


    def action_with_lots_or_refresh(self, session, access_token, driver):
        """
        Читает номера лота из lot_numbers.txt, если его нет - добавляет в файл и подаёт заявку,
        если есть - удаляет карточки лота. Если не находится лот, то происходит парсинг
        :return: Ничего не возвращает.
        """
        while True:
            lot_items_data = self.find_lots(session, access_token)
            if len(lot_items_data["items"]) == 0:
                print("Новые лоты не найдены")
                time.sleep(2)
            elif len(lot_items_data["items"]) > 0:
                trade_number = lot_items_data["items"][0]["tradeNumber"]
                lot_id = lot_items_data["items"][0]["id"]
                print("Найденный лот: ", trade_number)
                print("GUID лота:", lot_id)
                with open('lot_numbers.txt', 'r', encoding='utf-8') as r:
                    if trade_number in r.read():
                        print("Данный лот уже есть в lot_numbers.txt")
                    else:
                        with open('lot_numbers.txt', 'a', encoding='utf-8') as f:
                            f.write(trade_number + '\n')
                            winsound.Beep(1000, 1000)
                            cart_lot = self.get_cart_lot(session, lot_id, access_token)
                            print("Карточка лота:", cart_lot)
                            documents = self.find_documents_from_repository(session, access_token)
                            print("Документы:", documents)
                            tax = self.set_not_taxed(session=session, access_token=access_token, price=0.01)
                            print("Налог:", tax)
                            application_id = cart_lot["info"]["id"]
                            print("id предложения:", application_id)
                            sign_info = self.get_sign_info(session=session, access_token=access_token)
                            print(sign_info)
                            thumbprint = sign_info["thumbprints"][0]
                            print(thumbprint)

                            # TODO подача заявки на лот
                break
