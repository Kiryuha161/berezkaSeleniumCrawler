import psutil
import time
import winsound

from Classes.Bot import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Controller


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
        print("В зависимости от указанной базовой цены будет происходить установка цены на лот.")
        base_price = input("Введите базовую цену, которую необходимо подать: ")  # 0.01 или 1 или другую для теста

        bot = Bot()
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

        # bot.fill_inn_field(driver, inn)
        # bot.choice_inn_popup(driver, inn)
        bot.fill_search_text_field(driver, "Оказание услуг по реализации арестованного имущества -оценка -оценки "
                                           "-оценке -оценкой -хранение -хранении -хранения -хранением")
        # bot.fill_search_text_field(driver, "100219253124100051") тест, заменить номер

        refresh_btn = bot.click_by_search(driver, 3)
        bot.action_with_lots_or_refresh(driver, refresh_btn)

        bot.remove_date_end_application(driver)
        bot.add_documents_from_repository(driver)
        bot.set_price(driver, base_price)
        bot.click_on_value_added_tax(driver)

        if driver.find_elements(By.CLASS_NAME, "select-tru__icon"):
            # нашёл только в стилях
            bot.click_by_element_from_elements(driver, "select-tru__icon", 0)

            # этого вообще не нашёл
            bot.click_by_element_from_elements(driver, "tru-description-modal__action", 1)
            time.sleep(2)

            bot.click_on_add_offer(driver)
        else:
            time.sleep(1)

        print("Назначение кнопки")
        send = driver.find_element(By.XPATH, "//button[contains(text(), 'Подать предложение')]")
        print("Скролл")
        driver.execute_script("window.scrollTo(0, 10000)")
        send.click()

        while True:
            if driver.find_elements(By.CLASS_NAME, "c-btn--secondary"):
                driver.find_elements(By.CLASS_NAME, "c-btn--secondary")[1].click()
                break
            else:
                time.sleep(1)

        time.sleep(2)

        kb = Controller()

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
    kill_chrome_processes()
    main()
