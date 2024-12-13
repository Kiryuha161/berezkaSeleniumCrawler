import psutil
import time
import winsound
import os
import threading

from Classes.Bot import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def kill_chrome_processes():
    """
    Завершение всех запущенных процессов Google Chrome.
    :return: Ничего не возвращает.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            proc.kill()


def remove_style(driver):
    while True:
        print("Второй поток")
        # Удаление стилей через JavaScript
        driver.execute_script("document.querySelectorAll('link[rel=\"stylesheet\"]').forEach(el => el.remove());")

        # Удаление изображений через JavaScript
        driver.execute_script("document.querySelectorAll('img').forEach(el => el.remove());")
        time.sleep(1)

def main():
    try:
        # inn = input("Введите ИНН: ")  # 7716642273
        print("В зависимости от указанной базовой цены будет происходить установка цены на лот.")
        base_price = input("Введите базовую цену, которую необходимо подать: ")  # 0.01 или 1 или другую для теста

        bot = Bot()
        options = bot.init_options()

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # remove_style_thread = threading.Thread(target=remove_style, args=(driver,))
        # remove_style_thread.start()

        # script = """
        #     Object.defineProperty(document, 'readyState', {
        #         get: function() {
        #             // Удаление стилей при загрузке страницы
        #             document.querySelectorAll('link[rel="stylesheet"]').forEach(el => el.remove());
        #             return 'complete';
        #         }
        #     });
        #     """
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        #
        # # Удаление изображений через JavaScript
        # driver.execute_script("document.querySelectorAll('img').forEach(el => el.remove());")
        bot.remove_style_by_js(driver)
        driver.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")
        bot.remove_style_by_js(driver)
        time.sleep(3)

        # После перехода на предыдущую страницу происходит перенаправление на другую страницу.
        # Ниже WebDriver проверяет, перенаправило ли на страницу входа, если пользователь не залогинен

        if "https://login.agregatoreat.ru/Account/Login" in driver.current_url:
            bot.remove_style_by_js(driver)
            bot.login_by_signature(driver)
            time.sleep(5)

            bot.monitor_element_presence(driver, "#orglist")
            bot.login_by_gosuslugi(driver)
        bot.remove_style_by_js(driver)
        # Страница с новыми лотами (где стоит статус Подача предложения)
        driver.get("https://agregatoreat.ru/purchases/new")
        bot.remove_style_by_js(driver)

        # bot.fill_inn_field(driver, inn)
        # bot.choice_inn_popup(driver, inn)
        # bot.fill_search_text_field(driver, "Оказание услуг по реализации арестованного имущества -оценка -оценки "
        #                                    "-оценке -оценкой -хранение -хранении -хранения -хранением")
        bot.fill_search_text_field(driver, "403000448124100008")  # тест, заменить номер

        refresh_btn = bot.click_by_search(driver, 3)

        bot.action_with_lots_or_refresh(driver, refresh_btn)

        start_time_work_with_application = time.time()
        bot.remove_style_by_js(driver)
        # bot.handle_resource_enable(options, 2)

        bot.remove_date_end_application(driver)
        bot.add_documents_from_repository(driver)
        bot.set_price(driver, base_price)
        bot.click_on_value_added_tax(driver)

        # bot.handle_resource_enable(options, 1)
        end_time_work_with_application = time.time()
        perform_work_with_application = end_time_work_with_application - start_time_work_with_application
        print(f"{perform_work_with_application=}")
        bot.remove_style_by_js(driver)
        if driver.find_elements(By.CLASS_NAME, "select-tru__icon"):
            bot.remove_style_by_js(driver)
            # нашёл только в стилях
            bot.click_by_element_from_elements(driver, "select-tru__icon", 0)

            # этого вообще не нашёл
            bot.click_by_element_from_elements(driver, "tru-description-modal__action", 1)
            time.sleep(2)

            bot.click_on_add_offer(driver)
        else:
            time.sleep(1)

        print("Назначение кнопки")
        if driver.find_element(By.XPATH, "//button[contains(text(), 'Подать предложение')]"):
            bot.remove_style_by_js(driver)
            send = driver.find_element(By.XPATH, "//button[contains(text(), 'Подать предложение')]")
            print("Скролл")
            driver.execute_script("window.scrollTo(0, 10000)")
            send.click()

        while True:
            bot.remove_style_by_js(driver)
            if driver.find_elements(By.CLASS_NAME, "c-btn--secondary"):
                driver.find_elements(By.CLASS_NAME, "c-btn--secondary")[1].click()
                break
            else:
                time.sleep(1)

        try:
            bot.remove_style_by_js(driver)
            sign_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "signButton"))
            )
            print("Элемент найден!")

            sign_button.click()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        bot.end_time = time.time()
        bot.perform_time = bot.end_time - bot.start_time
        print(f"{bot.perform_time=}")

        # kb = Controller()

        time.sleep(10000)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        winsound.Beep(1000, 300)
        winsound.Beep(1000, 300)


"""
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 370, 300)
    win.setWindowTitle("BEREZKA")
    label1 = QtWidgets.QLabel(win)
    label1.setText("ИНН заказчика")
    label1.resize(150, 18)
    label1.move(120, 50)
    inp = QtWidgets.QLineEdit(win)
    inp.show()
    inp.resize(270, 30)
    inp.move(50, 80)
    check = QtWidgets.QCheckBox(win)
    check.show()
    check.move(50, 120)
    label2 = QtWidgets.QLabel(win)
    label2.show()
    label2.setText("Подавать заявку автоматически")
    label2.resize(300, 18)
    label2.move(80, 125)
    button = QtWidgets.QPushButton(win)
    button.show()
    button.setText("Запуск")
    button.resize(200, 50)
    button.move(80, 200)
    win.show()
    sys.exit(app.exec_())
"""

if __name__ == '__main__':
    # window()
    # При запущенных процессах хрома WebDriver не создаёт сессию, поэтому перед запуском бота убиваются процессы хрома
    kill_chrome_processes()
    main()
