from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import time
"""
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 500, 500)
    win.setWindowTitle("BEREZKA")

    label = QtWidgets.QLabel(win)
    label.setText("ИНН заказчика")
    label.move(200, 50)

    inp = QtWidgets.QI(win)
    inp.show()
    inp.move(200, 60)

    win.show()
    sys.exit(app.exec_())
"""
def main():
    options = Options()
    options.add_argument("--user-data-dir=C:\\Users\\igors\\Desktop\\BEREZKA\\UserData")
    options.page_load_strategy = 'normal'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    #driver.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")
    #time.sleep(5)
    driver.get("https://agregatoreat.ru/purchases/new")
    time.sleep(5)

    # options2 = Options()
    # options2.add_argument("--user-data-dir=C:\\Users\\igors\\Desktop\\BEREZKA\\UserData2")
    # options2.page_load_strategy = 'normal'
    # driver2 = webdriver.Chrome(options=options2)
    # driver2.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")
    # time.sleep(5)

    text_field1 = driver.find_element(By.ID, "filterField-14-autocomplete")
    text_field1.send_keys("7716642273")  # Сюда ввести нужный ИНН
    time.sleep(2)
    autocomp = driver.find_element(By.ID, "pr_id_2_list")
    autocomp.click()
    #text_field2 = driver.find_element(By.ID, "filterField-2-input")
    #text_field2.send_keys("реал")


    refresh_btn = driver.find_element(By.ID, "applyFilterButton")
    refresh_btn.click()
    time.sleep(2)

    while True:
        if driver.find_elements(By.ID, "applicationSendButton"):
            driver.find_element(By.ID, "applicationSendButton").click()
            break
        else:
            refresh_btn.click()
            time.sleep(1)

    time.sleep(7) # Ожидание прогрузки страницы торга

    price = driver.find_element(By.ID, "lotItemPriceInput-0")
    nds = driver.find_elements(By.TAG_NAME, "p-dropdown")

    for i in range(20):
        price.send_keys(Keys.BACKSPACE)

    price.send_keys("0,01")
    nds[1].click()

    move = ActionChains(driver).move_to_element_with_offset(nds[1], 10, 40)
    move.click()
    move.perform()

    if driver.find_elements(By.CLASS_NAME, "select-tru__icon"):
        tru = driver.find_elements(By.CLASS_NAME, "select-tru__icon")
        tru[0].click()

        truOption = driver.find_elements(By.CLASS_NAME, "tru-description-modal__action")
        truOption[1].click()

        time.sleep(2)

        truBtn = driver.find_element(By.ID, "add-offer")
        truBtn.click()
        time.sleep(10000)
    else:
        time.sleep(10000) # Тестовое значение (максимум 5 при реальном заупске)
"""
    Подать предложение (последняя кнопка)

    send = driver.find_elements(By.TAG_NAME, "button")
    print(send)
    driver.execute_script("window.scrollTo(0, 10000)")
    send[3].click()

    time.sleep(10)
"""


if __name__ == '__main__':
    #window()
    main()
