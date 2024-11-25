import json
import requests
import time
import winsound

from Objects.search import search_model
from Objects.headers import get_headers
from Objects.document_request import document_request_model

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

    def send_get_request(self, url, access_token):
        """
        Отправка get-запроса.
        :param url: Адрес запроса.
        :param access_token: Докен доступа.
        :return: Ответ на запрос или None
        """
        headers = get_headers(access_token)
        response = requests.get(url, headers=headers)

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

    def send_post_request(self, url, access_token, request_model=None):
        """
        Отправляет post-запрос.
        :param url: Адрес запроса.
        :param access_token: Докен доступа.
        :param request_model: Модель запроса, передаваемая в параметры.
        :return: Ответ на запрос или None
        """
        headers = get_headers(access_token)

        response = requests.post(url, headers=headers, json=request_model)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None

    def find_lots(self, access_token):
        """
        Отправка текста поиска лотов.
        :param access_token: Докен доступа.
        :return: Объект с данными, найденных лотов.
        """

        url = "https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots"

        lots_data = self.send_post_request(url, access_token, search_model)

        return lots_data

    def send_application(self):
        print("Подача предложения")
        # TODO сделать подачу заявки

    def find_documents_from_repository(self, access_token):
        """
        Находит документы из хранилища.
        :param access_token: Докен доступа.
        :return: Объект с данными найденных документов.
        """
        url = "https://registry-api.agregatoreat.ru/api/OrganizationDocuments/get-list"

        documents_data = self.send_post_request(url, access_token, document_request_model)

        return documents_data

    def get_cart_lot(self, lot_id, access_token):
        """
        Получение данных о лоте (получение карточки лота)
        :param lot_id: GUID для искомого лота.
        :param access_token: Токен доступа.
        :return:
        """
        url = f"https://tender-api.agregatoreat.ru/api/Application/new/{lot_id}"

        card_lot = self.send_get_request(url, access_token)

        return card_lot

    def action_with_lots_or_refresh(self, access_token):
        """
        Чтение номера лота из lot_numbers.txt, если его нет - добавление в файл и подача заявки,
        если есть - удаление карточки лота. Если не находится лот, то парсинг
        :return: Ничего не возвращает.
        """
        while True:
            lot_items_data = self.find_lots(access_token)
            if len(lot_items_data["items"]) == 0:
                print("Новые лоты не найдены")
                time.sleep(2)
            elif len(lot_items_data["items"]) > 0:
                trade_number = lot_items_data["items"][0]["tradeNumber"]
                lot_id = lot_items_data["items"][0]["id"]
                print("Найденный лот: ", trade_number)
                with open('lot_numbers.txt', 'r', encoding='utf-8') as r:
                    if trade_number in r.read():
                        print("Данный лот уже есть в lot_numbers.txt")
                    else:
                        with open('lot_numbers.txt', 'a', encoding='utf-8') as f:
                            f.write(trade_number + '\n')
                            winsound.Beep(1000, 1000)
                            card_lot = self.get_cart_lot(lot_id, access_token)
                            print(card_lot)

                            # TODO подача заявки на лот
                break