import asyncio
import json
import time
import threading
import websockets

from requests import Session
from selenium.webdriver.chrome.webdriver import WebDriver
from urllib.parse import urlsplit, parse_qs

from Objects.document_request import document_request_model
from Objects.headers import get_headers
from Objects.search import search_model
from Objects.tax_request import get_tax
from Objects.lot import get_lot


# Проверить сохранение черновика (документы)
class RequestBot:
    """Класс, отвечающий за работу бота, подающего предложения через запросы, а не через интерфейс."""

    def __init__(self):
        self.token = None
        self.prevToken = None
        self.info = None
        self.supplier = None
        self.trade = None
        self.document = None
        self.application_id = None
        self.contact_info = None
        self.ids = None
        self.print_form = None
        self.web_socket = None

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
            print(f"Статус: {response.status_code}")
            print(f"{response.text=}")
            print(f"{response.reason=}")
            print(f"{response.headers=}")
            return response.json()

        print(f"Статус: {response.status_code}")
        print(f"{response.text=}")
        print(f"{response.reason=}")
        print(f"{response.headers=}")
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
            print(f"Статус: {response.status_code}")
            print(f"{response.text=}")
            print(f"{response.reason=}")
            print(f"{response.headers=}")
            return response.json()

        print(f"Статус: {response.status_code}")
        print(f"{response.text=}")
        print(f"{response.reason=}")
        print(f"{response.headers=}")
        return

    @staticmethod
    def send_post_with_headers(session, url, headers, json_data=None):
        start_time = time.time()

        response = session.post(url, headers=headers, json=json_data)

        end_time = time.time()

        print(f"\nPOST запрос к {url} занял {end_time - start_time:.4f} секунд")

        if response.status_code == 200:
            print(f"Статус: {response.status_code}")
            print(f"{response.text=}")
            print(f"{response.reason=}")
            print(f"{response.headers=}")
            return response.json()

        print(f"Статус: {response.status_code}")
        print(f"{response.text=}")
        print(f"{response.reason=}")
        print(f"{response.headers=}")
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

        json_data = {
            "tradeLotId": "bb0a3250-0ae0-45ca-a69a-354235625beb",
            "applicationId": "d6d34658-7a55-46b1-8cae-6d128a748b2b",
            "contactPerson": "Кузнецова  Ксения Геннадиевна",
            "contactData": "тел. +7(989)621-05-03, sperik_ice@mail.ru",
            "isAgreeToSupply": True,
            "deliveryPrice": 0,
            "documents": [
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

    def get_data_for_sign(self, session, access_token, application_id: str, token: str, oid: str):
        """
        Получение данных для подписания
        :param session: Сессия requests.
        :param access_token: Токен доступа.
        :param application_id:
        :param token:
        :param oid: ОИД
        :return: Объект с данными ответа.
        """
        print("Получение данных для подписания")
        url = "https://tender-api.agregatoreat.ru/api/Application/data-for-sign"
        json_data = {
            "applicationId": application_id,
            "token": token,
            "oid": oid  # "1.2.643.7.1.1.1.1"
        }

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru,en;q=0.9",
            "authorization": f"Bearer {access_token}",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "content-type": "application/json",
            "host": "tender-api.agregatoreat.ru",
            "origin": "https://agregatoreat.ru",
            "pragma": "no-cache",
            "referer": "https://agregatoreat.ru/",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"
        }

        print(f"json_data: {json_data["applicationId"]=}, {json_data["token"]=}, {json_data["oid"]=}")
        # return self.send_post_request(session=session, url=url, access_token=access_token, json_data=json_data)
        return self.send_post_with_headers(session, url, headers, json_data)

    def save_draft_application(self, session, access_token, ids, contact_info, document, price, trade, info):
        url = "https://tender-api.agregatoreat.ru/api/Application/draft?validate=false"
        lot = get_lot(ids, contact_info, document, price, trade, info)
        print("lot", lot)

        return self.send_post_request(session=session, url=url, access_token=access_token, json_data=lot)

    def generate_print_form(self, session, access_token, application_id, token):
        url = f"https://tender-api.agregatoreat.ru/api/Application/{application_id}/print-form/{token}"
        return self.send_get_request(session=session, url=url, access_token=access_token)

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

        # @staticmethod

    async def listen_websockets(self, credentials, session, trade, application_id, document, info, contact_info, ids):
        wss_url = (
            f"wss://signalr.agregatoreat.ru/AuthorizedHub?id={credentials['id']}&v={credentials['v']}"
            f"&access_token={credentials['access_token']}"
        )

        print(f'\nПопытка запустить обмен по websockets')
        retry_count = 10
        retry_delay = 2  # seconds
        for attempt in range(retry_count):
            try:
                async with websockets.connect(wss_url) as websocket:
                    print(f"{websocket=}")
                    print(
                        'Соединение по websockets прошло успешно. '
                        'Попытка отправить первое сообщение -> {"protocol":"json","version":1}'
                    )
                    await websocket.send('{"protocol":"json","version":1}\x1e')
                    print('Первое сообщение отправлено. Ждем ответ')
                    response = await websocket.recv()
                    print(f'Ответ получен {response}')
                    print(f'Переходим в бесконечный цикл обмена сообщениями')
                    if application_id is not None:
                        draft_response = self.save_draft_application(
                            session=session,
                            access_token=credentials['access_token'],
                            ids=ids,
                            contact_info=contact_info,
                            document=document,
                            price=0.01,
                            trade=trade,
                            info=info
                        )
                        print(f"{draft_response=}")

                    if self.token is not None:
                        self.prevToken = token
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
                                token = response["arguments"][-1]  # [1]
                                self.token = token
                                print(f"Токен обновлен в первый раз: {token}")
                                if application_id is not None and self.print_form is None:
                                    print_form = self.generate_print_form(
                                        session=session,
                                        access_token=credentials["access_token"],
                                        application_id=application_id,
                                        token=self.token
                                    )
                                    print(f"{print_form}")
                                    self.print_form = print_form

                                if response["target"] == "ApplicationPrintFormGenerated":
                                    token = response["arguments"][-1]  # [1]
                                    self.token = token
                                    print("Второе обновление токена", token)
                                    data_for_sign = self.get_data_for_sign(
                                        session=session,
                                        access_token=credentials['access_token'],
                                        application_id=application_id,
                                        token=self.token,
                                        oid="1.2.643.7.1.1.1.1"
                                    )

                                    print(f"{data_for_sign=}")
                            else:
                                print('Ничего интересного пропускаем')
                        except Exception as ex:
                            print("Ошибка", ex)
                    break   # Если соединение успешно, выходим из цикла повторных попыток
            except(websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidStatusCode) as e:
                print(f"Ошибка подключения к WebSocket: {e}. Попытка {attempt + 1} из {retry_count}")
                if attempt < retry_count - 1:
                    print(f"Повторная попытка через {retry_delay} секунд...")
                    await asyncio.sleep(retry_delay)
                else:
                    print("Превышено количество попыток подключения.")
                    break

    def action_with_lots_or_refresh(self, session: Session, access_token: str, driver: WebDriver):
        """
        Парсинг и выкуп лотов.
        Если лота нет среди purchased_lots и у него не фиксированная цена, то идут запросы для подачи заявки за 0.01.
        :return: Ничего
        """
        # Получаем куки из веб-драйвера
        selenium_cookies = self.get_cookies(driver)

        # Преобразуем куки в формат, который может использовать requests
        requests_cookies = {}
        for cookie in selenium_cookies:
            requests_cookies[cookie['Name']] = cookie['Value']

        # Устанавливаем куки в объект сессии
        session.cookies.update(requests_cookies)
        print("cookie:", session.cookies)

        ws_connection = self.get_websockets_from_selenium(driver)
        print(f"Информация для доступа к вебсокету {ws_connection}")

        # Запуск асинхронной функции в отдельном потоке
        def run_websocket_listener():
            asyncio.run(
                self.listen_websockets(
                    {
                        'id': ws_connection["id"],
                        'v': ws_connection["v"],
                        'access_token': ws_connection["access_token"]
                    },
                    session=session,
                    trade=self.trade,
                    application_id=self.application_id,
                    document=self.document,
                    info=self.info,
                    ids=self.ids,
                    contact_info=self.contact_info
                )
            )

        # Документ
        account_documents = self.find_documents_from_repository(session, access_token)  # TODO хз как работает
        document = account_documents["items"][0]
        document["documentName"] = "Документы"
        self.document = document

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
            if not lot_full_info:
                time.sleep(1)
                continue

            self.application_id = lot_full_info["info"]["id"]
            print(f"{self.application_id=}")

            self.trade = lot_full_info["trade"]
            print(f"{self.trade=}")
            self.info = lot_full_info["info"]
            print(f"{self.info=}")
            self.supplier = lot_full_info["supplier"]
            print(f"{self.supplier=}")

            self.ids = {
                "trade_lot": self.info["tradeLotId"],
                "application": self.application_id
            }
            print(f"{self.ids["trade_lot"]=}")
            print(f"{self.ids["application"]=}")

            self.contact_info = {
                "person": self.supplier["contactFio"],
                "data": f"{self.supplier["phoneNumber"]}, {self.supplier["email"]}"
            }

            websocket_thread = threading.Thread(target=run_websocket_listener)
            websocket_thread.start()

            # Добавляем в переменную последний купленный лот
            purchased_lots.append(lot_id)
            print(f"Общая работа {time.time() - st:.4f} секунд")

            break  # TODO: В проде нужно будет удалить
