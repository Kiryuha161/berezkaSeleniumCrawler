import asyncio
import json
import time
from urllib.parse import urlsplit, parse_qs

import websockets
from requests import Session
from selenium.webdriver.chrome.webdriver import WebDriver

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
    def get_access_token(local_storage_items) -> str:
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
    def send_get_request(session, url, access_token) -> dict | None:
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
    def send_post_request(session, url, access_token, json_data=None, cookie=None) -> dict | None:
        """
        Отправляет post-запрос.
        :param session: Сессия requests.
        :param url: Адрес запроса.
        :param access_token: Токен доступа.
        :param json_data: Передаваемые в параметры.
        :param cookie: Куки.
        :return: Ответ на запрос или None.
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

    def set_document(self, session, access_token, document):
        """
        Устанавливает документ в лот
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :param document: Документ.
        :return: Объект с данными ответа.
        """
        url = "https://tender-api.agregatoreat.ru/api/Application/draft?validate=false"

        # TODO: !!! Пример из запроса, а не корректные данные !!!
        # для этого заказа, если важно https://agregatoreat.ru/purchases/application/price-request/b5214d7f-dfd7-4926-a7dc-23dcafbed771  # noqa
        json_data = {
            "tradeLotId": "bb0a3250-0ae0-45ca-a69a-354235625beb",
            "applicationId": "d6d34658-7a55-46b1-8cae-6d128a748b2b",
            "contactPerson": "Кузнецова  Ксения Геннадиевна",
            "contactData": "тел. +7(989)621-05-03, sperik_ice@mail.ru",
            "isAgreeToSupply": True,
            "deliveryPrice": 0,
            "documents": [
                # { # Заполнил данными документа, что смог
                #     "id": document["id"],
                #     "type": 0,  # TODO: хз
                #     "size": document["fileSize"],
                #     "name": document["fileName"],
                #     "version": None,
                #     "isActual": None,
                #     "typeName": None,
                #     "documentName": None,
                #     "createdOn": "",  # TODO: текущее время
                #     "sendDate": None
                # }
                {
                    "id": "a87c577c-97bf-4735-82ba-e890663c5d0e",
                    "type": 0,
                    "size": 6356006,
                    "name": "Заявки Транстех Березка.zip",
                    "version": None,
                    "isActual": None,
                    "typeName": None,
                    "documentName": None,
                    "createdOn": "2024-12-02T20:12:22Z",
                    "sendDate": None
                }
            ],
            "items": [
                {
                    "quotation": 15500,
                    "quantity": 38,
                    "tradeLotItemOrder": 0,
                    "taxPercent": 1000,
                    "name": "Оказание услуг по переезду",
                    "offerId": "00000000-0000-0000-0000-000000000000",
                    "offerNumber": None,
                    "countryOfOrigin": None,
                    "isPriceWithTax": True,
                    "calculatedTax": 0,
                    "sum": 589000,
                    "offerName": None,
                    "description": "В соответствии с проектом контракта ",
                    "offerDescription": None,
                    "priceOption": 1,
                    "requireOfferSpecification": False,
                    "russianItemsRegistryNum": None,
                    "russianItemsRegistry": None,
                    "isSelected": False,
                    "referenceOfferId": None,
                    "referenceOfferNumber": None,
                    "isReference": False
                }
            ],
            "applicationSubType": 0,
            "applicationPriceHidden": False,
            "sessionConclusionContractPrice": None,
            "decreasePercent": None,
            "unitPriceSum": 15500,
            "calculatedTax": 0,
            "taxPercent": 0
        }

        return self.send_post_request(
            session=session,
            url=url,
            access_token=access_token,
            json_data=json_data
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

    @staticmethod
    def get_websockets_from_selenium(driver) -> dict[str, str] | None:
        """
        Получение данных из логов, для запроса к вебсокету
        :param driver:
        :return: Словарь с данными, для последующего запроса к вебсокету
        """
        print("\nПолучаем сообщения об авторизации webSocket из лога браузера")
        st = time.time()

        for wsData in driver.get_log('performance'):
            wsJson = json.loads((wsData['message']))

            if wsJson["message"]["method"] == "Network.webSocketCreated":
                url = urlsplit(wsJson["message"]["params"]["url"])
                if (
                        'signalr.agregatoreat.ru'.upper() in url.netloc.upper()
                        and 'AuthorizedHub'.upper() in url.path.upper()
                ):
                    query = parse_qs(url.query)

                    print(f"Работа по поиску данных для вебсокета: {time.time() - st:.4f} секунд")
                    return {
                        'id': query.get('id', [''])[0],
                        'v': query.get('v', [''])[0],
                        'access_token': query.get('access_token', [''])[0],
                    }

    @staticmethod
    async def listen_websockets(credentials):
        wss_url = (
            f"wss://signalr.agregatoreat.ru/AuthorizedHub?id={credentials['id']}&v={credentials['v']}"
            f"&access_token={credentials['access_token']}"
        )

        print(f'\nПопытка запустить обмен по websockets')
        async with websockets.connect(wss_url) as websocket:
            print(
                'Соединение по websockets прошло успешно. '
                'Попытка отправить первое сообщение -> {"protocol":"json","version":1}'
            )
            await websocket.send('{"protocol":"json","version":1}\x1e')
            print('Первое сообщение отправлено. Ждем ответ')
            response = await websocket.recv()
            print(f'Ответ получен {response}')
            print(f'Переходим в бесконечный цикл обмена сообщениями')
            while True:
                raw_response = await websocket.recv()
                print(f'Получили сырое сообщение -> {raw_response}')
                try:
                    print('Парсим сообщение')
                    response = json.loads(raw_response.replace('\x1e', ''))
                    print(f"\n{response=}")
                    if response['type'] == 6:
                        print('Получили служебное сообщение отправляем ответ <- {"type":6}')
                        await websocket.send('{"type":6}\x1e')
                    elif response['type'] == 1 and 'arguments' in response:
                        print(f'Получили сообщение о различных токенах лота {response["arguments"]}')
                        # TODO: вот тут что-то надо делать
                        token = response["arguments"].get("token")
                        print(f"Токен обновлен: {token}")

                        # for order in list_number_procedure:
                        #     callback(order, now)
                    else:
                        print('Ничего интересного пропускаем')

                except Exception as ex:
                    print("Ошибка", ex)

    def action_with_lots_or_refresh(self, session: Session, access_token: str, driver: WebDriver):
        """
        Парсинг и выкуп лотов.
        Если лота нет среди purchased_lots и у него не фиксированная цена, то идут запросы для подачи заявки за 0.01.
        :return: Ничего
        """

        ws_connection = self.get_websockets_from_selenium(driver)
        print(f"Информация для доступа к вебсокету {ws_connection}")

        # TODO: вебсокет почему то не всегда с первой попытки запускается

        # После какого либо действия в лоте, например установления цены или прикрепить файл, сокет будет периодические
        # слать что-то типо такого
        # {"type":1,"target":"ApplicationDraftSaved","arguments":["9893e5e4-a909-4d6b-9786-3772f4cdcff1","f399e1ac-a297-4c86-a31f-c080ca35bf33"]}
        # Первый - это applicationId, второй - это token для data-for-sign

        # TODO: Либо нужно вебсокеты запускать где-то как-то отдельно и читать что там происходит,
        #  либо перенести функцию по чтению сообщений в вебсокете внутрь цикла, после всех действий в лоте

        # Запуск асинхронной функции
        asyncio.run(
            self.listen_websockets(
                {
                    'id': ws_connection["id"],
                    'v': ws_connection["v"],
                    'access_token': ws_connection["access_token"]
                }
            )
        )

        # Документ
        account_documents = self.find_documents_from_repository(session, access_token)  # TODO хз как работает
        document = account_documents["items"][0]
        print("Документы:", account_documents)
        print("Документ:", document)

        purchased_lots = []  # переменная для хранения выкупленных лотов
        while True:
            st = time.time()

            items: list[dict] = self.find_lots(session, access_token)["items"]

            if not items:
                print("Новые лоты не найдены")
                time.sleep(1)
                continue

            buy_item = None  # лот который можно купить
            for item in items:
                # Если лот уже был выкуплен нами
                if item["id"] in purchased_lots:
                    continue

                # проверка, что есть товары, что бы в дальнейшем предотвратить ошибку
                items = item["lotItems"]
                if not items:
                    continue

                # TODO: можно попробовать добавить проверку на то выкупил ли уже кто нибудь лот по минимальной цене (len(items) * 0.01)  # noqa

                need_continue = False  # переменная для прерывания цикла

                # проверка, что у всех товаров Лота можно отредактировать цену
                for lot_item in items:
                    if lot_item["priceOption"] == 2:  # 2 означает что нельзя изменить цену, 1 - что можно
                        need_continue = True
                        break

                if need_continue:
                    continue

                # Этот лот можно купить
                buy_item = item
                break

            if not buy_item:
                print("Новые лоты не найдены")
                time.sleep(1)
                continue

            trade_number = buy_item["tradeNumber"]
            lot_id = buy_item["id"]
            print("\nНайденный лот: ", trade_number)
            print("GUID лота:", lot_id)

            # Не понятно как передать в эту карточку значения некоторых свойств,
            # возможно следующие запросы меняют это значение в базе данных?
            lot_full_info = self.get_cart_lot(session, lot_id, access_token)
            print("Карточка лота:", lot_full_info)
            if not lot_full_info:
                time.sleep(1)
                continue

            application_id = lot_full_info["info"]["id"]
            print("id предложения:", application_id)

            self.set_document(session=session, access_token=access_token, document=document)  # TODO ОБЯЗАТЕЛЬНО ДОДЕЛАТЬ

            tax = self.set_not_taxed(session=session, access_token=access_token, price=0.01)  # TODO хз как работает
            print("Налог:", tax)

            sign_info = self.get_sign_info(session=session, access_token=access_token)  # TODO а нужно ли ?
            print(sign_info)
            thumbprint = sign_info["thumbprints"][0]
            print("Отпечаток подписи:", thumbprint)

            # подача заявки на лот
            # self.send_application(
            #     session,
            #     access_token,
            #     application_id,
            #     token, # TODO: нужно получит как то
            #     oid # TODO: нужно получит как то
            # )

            # Добавляем в переменную последний купленный лот
            purchased_lots.append(lot_id)
            print(f"Общая работа {time.time() - st:.4f} секунд")

            break  # TODO: В проде нужно будет удалить
