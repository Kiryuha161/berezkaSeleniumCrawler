import psutil
import time

import winsound

from Classes.Bot import Bot
from Classes.RequestBot import RequestBot

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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

        request_bot.action_with_lots_or_refresh(local_storage_items)

        time.sleep(1000000)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        winsound.Beep(1000, 300)
        winsound.Beep(1000, 300)

if __name__ == '__main__':
    #window()
    kill_chrome_processes()
    main()
