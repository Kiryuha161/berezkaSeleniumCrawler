import psutil
import time
import requests
import winsound

from Classes.Bot import Bot
from Classes.RequestBot import RequestBot

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def kill_chrome_processes():
    """
    Завершает все запущенные процессы Google Chrome
    :return: ничего не возвращает.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            proc.kill()

def main():
    try:
        # Есть две версии бота, один обычный через UI, другой через запросы (этот).
        # Однако запуск бота и там и там происходит одинаково, поэтому тут тоже есть экземпляр класса обычного бота.
        bot = Bot()
        request_bot = RequestBot()
        options = bot.init_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print("Бот и WebDriver проинициализированы успешно!")

        driver.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")
        time.sleep(3)

        # После перехода на предыдущую страницу происходит перенаправление на другую страницу.
        # Ниже WebDriver проверяет перенаправило ли на страниц входа, если пользователь не залогинен

        if "https://login.agregatoreat.ru/Account/Login" in driver.current_url:
            bot.login_by_signature(driver)
            time.sleep(5)

            bot.monitor_element_presence(driver, "#orglist")
            bot.login_by_gosuslugi(driver)

        # Страница с новыми лотами (где стоит статус Подача предложения)
        driver.get("https://agregatoreat.ru/purchases/new")

        local_storage_items = request_bot.get_local_storage(driver)
        access_token = request_bot.get_access_token(local_storage_items)
        print(f"access_token", access_token)

        cart_id = request_bot.get_cart_id(local_storage_items)
        print(f"cart_id", cart_id)

        # Метод, где происходят  все основные действия с лотами
        with requests.Session() as session:
            request_bot.action_with_lots_or_refresh(session, access_token, driver)

        time.sleep(1000000)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        winsound.Beep(1000, 300)
        winsound.Beep(1000, 300)

if __name__ == '__main__':
    # При запущенных процессах хрома WebDriver не создаёт сессию, поэтому перед запуском бота убиваются процессы хрома
    kill_chrome_processes()
    main()
