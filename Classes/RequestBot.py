import json
import time

import winsound

from Objects.document_request import document_request_model
from Objects.headers import get_headers
from Objects.search import search_model
from Objects.tax_request import get_tax


class RequestBot:
    """Класс, отвечающий за работу бота, подающего предложения через запросы, а не через интерфейс."""

    @staticmethod
    def get_cookies(driver):
        """
        Получает куки.
        :param driver: Экземпляр веб-драйвера Selenium, используемый для взаимодействия с веб-страницей.
        :return: Объект с куки
        """
        return [{"Name": cookie["name"], "Value": cookie["value"]} for cookie in driver.get_cookies()]

    @staticmethod
    def get_local_storage(driver):
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
        return driver.execute_script(script)

    @staticmethod
    def get_access_token(local_storage_items):
        """
        Получает токен доступа.
        :param local_storage_items: Объект со всеми значениями локального хранилища.
        :return: Токен доступа.
        """
        authorization_data = local_storage_items['0-eat_ui']
        authorization_data_dict = json.loads(authorization_data)
        return authorization_data_dict['authnResult']['access_token']

    @staticmethod
    def get_cart_id(local_storage_items):
        """
        Получение id карточки лота
        :param local_storage_items: Объект со всеми значениями локального хранилища.
        :return: Токен доступа.
        """
        return local_storage_items['cart_id']

    @staticmethod
    def send_get_request(session, url, access_token):
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

        print(f"\nGET запрос к {url} занял {end_time - start_time:.4f} секунд")

        if response.status_code == 200:
            return response.json()

        print(f"Статус: {response.status_code}")
        print(response.text)
        return

    @staticmethod
    def send_post_request(session, url, access_token, json_data=None, cookie=None):
        """
        Отправляет post-запрос.
        :param session: Сессия requests.
        :param url: Адрес запроса.
        :param access_token: Токен доступа.
        :param json_data: Передаваемые в параметры.
        :param cookie: Куки.
        :return: Ответ на запрос или None
        """
        headers = get_headers(access_token)

        start_time = time.time()

        response = session.post(url, headers=headers, json=json_data)

        end_time = time.time()

        print(f"\nPOST запрос к {url} занял {end_time - start_time:.4f} секунд")

        if response.status_code == 200:
            return response.json()

        print(f"Статус: {response.status_code}")
        print(response.text)
        return

    def find_lots(self, session, access_token):
        """
        Отправка текста поиска лотов.
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными, найденных лотов.
        """
        url = "https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots"
        return self.send_post_request(session, url, access_token, search_model)

    def find_documents_from_repository(self, session, access_token, cookies=None):
        """
        Находит документы из хранилища.
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными найденных документов.
        """
        url = "https://registry-api.agregatoreat.ru/api/OrganizationDocuments/get-list"
        return self.send_post_request(
            session=session,
            url=url,
            access_token=access_token,
            json_data=document_request_model,
            cookie=cookies
        )

    def get_cart_lot(self, session, lot_id, access_token):
        """
        Получение данных о лоте (получение карточки лота)
        :param session: Сессия requests.
        :param lot_id: GUID для искомого лота.
        :param access_token: Токен доступа.
        :return: Объект с данными лота.
        """
        url = f"https://tender-api.agregatoreat.ru/api/Application/new/{lot_id}"
        return self.send_get_request(session, url, access_token)

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
        return self.send_post_request(
            session=session,
            url=url,
            access_token=access_token,
            json_data=tax_request_model
        )

    def get_sign_info(self, session, access_token):
        """
        Получает информацию о подписи
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :return: Объект с данными подписи.
        """
        url = "https://registry-api.agregatoreat.ru/api/User/self"
        return self.send_get_request(session=session, url=url, access_token=access_token)

    def send_application(self, session, access_token, application_id: str, token: str, oid: str):
        """
        Подача заявки о покупке лота
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :param application_id:
        :param token:
        :param oid: ОИД
        :return: Объект с данными ответа.
        """
        print("Подача предложения")
        url = "https://tender-api.agregatoreat.ru/api/Application/data-for-sign"
        json_data = {
            "applicationId": application_id,  # "b7e35ad2-f8b2-461b-b484-e2db542c369b",
            "token": token,  # "f334dc87-bad7-4ff9-84b0-213b53a68d5f",
            "oid": oid  # "1.2.643.7.1.1.1.1"
        }
        return self.send_post_request(session=session, url=url, access_token=access_token, json_data=json_data)

    def action_with_lots_or_refresh(self, session, access_token, driver):
        """
        Читает номера лота из lot_numbers.txt, если его нет - добавляет в файл и подаёт заявку,
        если есть - удаляет карточки лота. Если не находится лот, то происходит парсинг
        :return: Ничего не возвращает.
        """

        last_item_id = None  # переменная для хранения последнего лота
        while True:

            st = time.time()
            start_time = time.time()

            items: list[dict] = self.find_lots(session, access_token)["items"]

            print(f"Часть работы, поиск лотов {time.time() - start_time:.4f} секунд")

            if not items:
                print("Новые лоты не найдены")
                time.sleep(2)
                continue

            # будет обрабатываться всегда первый ... или это не проблема ?
            buy_item = None  # лот который можно купить
            need_continue = False  # переменная для прерывания цикла
            for item in items:
                # Если итерация дошла до уже исследованного Лота
                if item["id"] == last_item_id:
                    need_continue = True
                    break

                # проверка, что есть товары, что бы в дальнейшем предотвратить ошибку
                items = item["lotItems"]
                if not items:
                    break

                need_continue_2 = False  # переменная для прерывания цикла

                # проверка, что у всех товаров Лота можно отредактировать цену
                for lot_item in items:
                    if lot_item["priceOption"] == 2:  # 2 означает что нельзя изменить цену, 1 - что можно
                        need_continue_2 = True
                        break

                if need_continue_2:
                    continue

                # Этот лот можно купить
                buy_item = item
                break

            if need_continue:
                print("Новые лоты не найдены")
                time.sleep(2)
                continue

            trade_number = buy_item["tradeNumber"]
            lot_id = buy_item["id"]
            print("\nНайденный лот: ", trade_number)
            print("GUID лота:", lot_id)
            start_time = time.time()

            # Не понятно как передать в эту карточку значения некоторых свойств,
            # возможно следующие запросы меняют это значение в базе данных?
            lot_full_info = self.get_cart_lot(session, lot_id, access_token)
            print("Карточка лота:", lot_full_info)
            application_id = lot_full_info["info"]["id"]
            print("id предложения:", application_id)

            print(f"Часть работы, инфа о лоте {time.time() - start_time:.4f} секунд")
            start_time = time.time()

            account_documents = self.find_documents_from_repository(session, access_token)
            document = account_documents["items"][0]
            print("Документы:", account_documents)
            print("Документ:", document)
            print(f"Часть работы, поиск документов {time.time() - start_time:.4f} секунд")
            start_time = time.time()

            tax = self.set_not_taxed(session=session, access_token=access_token, price=0.01)
            print("Налог:", tax)
            print(f"Часть работы, установка налога {time.time() - start_time:.4f} секунд")
            start_time = time.time()

            sign_info = self.get_sign_info(session=session, access_token=access_token)
            print(f"Часть работы, инфа о подписи {time.time() - start_time:.4f} секунд")
            print(sign_info)
            thumbprint = sign_info["thumbprints"][0]
            print("Отпечаток подписи:", thumbprint)

            print(f"Общая работа {time.time() - st:.4f} секунд")

            # TODO: осталось выяснить, что за токен в payload к запросу подписи

            # подача заявки на лот
            # self.send_application(
            #     session,
            #     access_token,
            #     application_id,
            #     token, # TODO: нужно получит как то
            #     oid # TODO: нужно получит как то
            # )

            # Меняем переменную на последний купленный лот
            last_item_id = buy_item["id"]

            break  # В проде нужно будет удалить
