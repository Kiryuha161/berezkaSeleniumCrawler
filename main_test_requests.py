import psutil
import time

import requests
import winsound
import json

from Bot import Bot
from RequestBot import RequestBot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Key, Controller


def kill_chrome_processes():
    """
    Завершение всех запущенных процессов Google Chrome.
    :return: ничего не возвращает.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            proc.kill()


def main():
    try:
        # inn = input("Введите ИНН: ")  # 7716642273
        # print("В зависимости от указанной базовой цены будет происходить установка цены на лот.")
        # base_price = input("Введите базовую цену, которую необходимо подать: ")  # 0.01 или 1 или другую для теста

        bot = Bot()
        request_bot = RequestBot()
        options = bot.init_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")
        time.sleep(3)

        if "https://login.agregatoreat.ru/Account/Login" in driver.current_url:
            bot.login_by_signature(driver)
            time.sleep(5)

            bot.monitor_element_presence(driver, "#orglist")
            bot.login_by_gosuslugi(driver)

        driver.get("https://agregatoreat.ru/purchases/new")

        # cookies = request_bot.get_cookies(driver)
        local_storage_items = request_bot.get_local_storage(driver)
        access_token = request_bot.get_access_token(local_storage_items)
        print(f"access_token", access_token)

        cart_id = request_bot.get_cart_id(local_storage_items)
        print(f"cart_id", cart_id)

        url1 = "https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjBDOTgyMzhGNEE3OUU3RjExN0U5OUJGMTQ4N0M5ODA0IiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2xvZ2luLmFncmVnYXRvcmVhdC5ydSIsIm5iZiI6MTczMTY3NjE1MywiaWF0IjoxNzMxNjc2MTUzLCJleHAiOjE3MzE2Nzk3NTMsImF1ZCI6InVpLWFwaSIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJ1aS1hcGkiXSwiYW1yIjpbInB3ZCJdLCJjbGllbnRfaWQiOiJlYXRfdWkiLCJzdWIiOiI5MmZiOWVkOC02NzYzLTQ3ODgtYWQ0NC1hMDI4NDczNmYzMWYiLCJhdXRoX3RpbWUiOjE3MzE2NzIyODUsImlkcCI6ImxvY2FsIiwib3JnYW5pemF0aW9uX2lkIjoiNjg1ODk2MzYtOGJkNS00NTg2LWFmOWYtODZlZTdlMDcwNjBiIiwiY2xpZW50X3R5cGUiOiJTdXBwbGllciIsInNpZCI6IjkwRTE4MkNCQ0VEMDM4ODlGNUI3RkVEMEI1OEMyM0RDIiwianRpIjoiNUY2NTBGREMzOEFBOTMyQTBENzk2MzA0REQ2RTU1NTUifQ.WfcFTNUvZBow2sfLgnQWjEMmOxGEJWHJQGKgAioG0NW9HJophk-XSkfsJAsEr2Ae5NiTeLQRETmCLXRezaPglKranFIwURXhGYMEqheONKxlrqkQBXsIoi-pZgojaYgg2SFmHdNU6BN0DZJcjKzVE8CF6xz8tj2CVdsvn2jG8ZnAmNFdIa8TjRdIXvrY51_ViDu0HWzGW76aQ9nFtRbZOGgOuQty1zuAE7Kosxpn1pzBTDXuuacuZzX6TVqoMzHitsnXjmRcne2DD2wWXnbbldR60sZ67jCTGcye0dfSMF3Cvy50XooWrW0JR3DXWsyLREnVO_amtEqV9Oy0Dkjb3A",
            "cache-control": "no-cache",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://agregatoreat.ru",
            "pragma": "no-cache",
            "referer": "https://agregatoreat.ru/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        payload = {
            "page": 1,
            "size": 10,
            "isReviewAwaiting": False,
            "isCustomerSendingAwaiting": False,
            "isCustomerSigningAwaiting": False,
            "isSupplierSigningAwaiting": False,
            "isSupplierAdditionalAgreementSignAwaiting": False,
            "isDealTerminationSignAwaiting": False,
            "isChangeDealTermsProtocolReceived": False,
            "isWinner": False,
            "isLoser": False,
            "searchText": "Оказание услуг по реализации арестованного имущества -оценка -оценки -оценке -оценкой -хранение -хранении -хранения -хранением",  # "Оказание услуг по реализации арестованного имущества -оценка -оценки -оценке -оценкой -хранение -хранении -хранения -хранением"
            "purchaseName": "",
            "number": None,
            "lotItemEatCodes": [],
            "productCode": None,
            "okpd2Codes": [],
            "ktruCodes": [],
            "purchaseTypeIds": [],
            "types": [],
            "customerId": None,
            "customerInn": None,
            "customerKpp": None,
            "supplierNameOrInn": None,
            "purchaseMethods": [],
            "priceStart": None,
            "priceEnd": None,
            "deliveryAddressRegionCodes": [],
            "deliveryAddress": None,
            "contractPriceStart": None,
            "contractPriceEnd": None,
            "applicationFillingStartDate": None,
            "applicationFillingEndDate": None,
            "contractSignDateStart": None,
            "contractSignDateEnd": None,
            "deliveryDateStart": None,
            "deliveryDateEnd": None,
            "isSmpOnly": False,
            "isEatOnly": True,
            "stateDefenseOrderOnly": None,
            "createDateTime": None,
            "excludeCancelledByCustomer": False,
            "excludeExternalTrades": False,
            "publishDateBegin": None,
            "publishDateEnd": None,
            "updateDateBegin": None,
            "updateDateEnd": None,
            "applicationFillingStartDateBegin": None,
            "applicationFillingStartDateEnd": None,
            "customerContractNumber": None,
            "hasLinkedExternalTrade": None,
            "eisTradeNumber": None,
            "isSpecificSupplier": False,
            "isRussianItemsPurchase": None,
            "organizerRegion": None,
            "organizerRegions": [],
            "etpType": None,
            "favoriteTag": None,
            "lotStates": [2],
            "sort": [
                {
                    "fieldName": "publishDate",
                    "direction": 2
                }
            ]
        }

        # Выполнение POST-запроса
        response = requests.post(url1, headers=headers, json=payload)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Получение данных в переменную
            data = response.json()
            print(data)
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)

        # разобраться чем отличаются запросы на странцие all, от запросов на странице new

        time.sleep(1000000)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        winsound.Beep(1000, 300)
        winsound.Beep(1000, 300)

if __name__ == '__main__':
    #window()
    kill_chrome_processes()
    main()
