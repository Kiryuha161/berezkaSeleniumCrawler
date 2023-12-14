import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

import time


def main():
    options = Options()
    cwd = os.getcwd().replace('/', '\\')
    options.add_argument(f"--user-data-dir={cwd}\\UserData")
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    driver.get("https://agregatoreat.ru/lk/supplier/eat/purchases/active/all")

    while True:
        if not driver.find_elements(By.CSS_SELECTOR, "#filterField-14-autocomplete"):
            while True:
                if driver.find_elements(By.CSS_SELECTOR, ".btn-block.mt-0"):
                    driver.find_elements(By.CSS_SELECTOR, ".btn-block.mt-0")[0].click()
                    break
                else:
                    time.sleep(1)

            while True:
                if driver.find_elements(By.CSS_SELECTOR, ".plain-button_light") and driver.find_elements(By.CSS_SELECTOR, ".plain-button_light")[1].get_attribute("innerText") == " Эл. подпись ":
                    driver.find_elements(By.CSS_SELECTOR, ".plain-button_light")[1].click()
                    while True:
                        if driver.find_elements(By.CSS_SELECTOR, ".plain-button_wide"):
                            driver.find_elements(By.CSS_SELECTOR, ".plain-button_wide")[0].click()
                            break
                        else:
                            time.sleep(1)
                    break
                else:
                    time.sleep(1)

            while True:
                if driver.find_elements(By.CSS_SELECTOR, "#searchFilterText"):
                    driver.get("https://agregatoreat.ru/purchases/new")
                    break
                else:
                    time.sleep(1)
        else:
            driver.get("https://agregatoreat.ru/purchases/new")
            break

    #time.sleep(100000)

    while True:
        if driver.find_elements(By.CSS_SELECTOR, "#filterField-14-autocomplete"):
            text_field1 = driver.find_elements(By.CSS_SELECTOR, "#filterField-14-autocomplete")[0]
            text_field1.send_keys("7708701670")  # Сюда ввести нужный ИНН
            break
        else:
            time.sleep(1)

    while True:
        if driver.find_elements(By.CSS_SELECTOR, "#pr_id_2_list"):
            autocomp = driver.find_elements(By.CSS_SELECTOR, "#pr_id_2_list")[0]
            autocomp.click()
            break
        else:
            time.sleep(1)

    # Фильтр по словам
    # text_field2 = driver.find_element(By.ID, "filterField-2-input")
    # text_field2.send_keys("реал")

    refresh_btn = driver.find_element(By.ID, "applyFilterButton")
    refresh_btn.click()
    time.sleep(3)

    while True:
        if driver.find_elements(By.ID, "tradeNumber"):
            lotNum = driver.find_element(By.ID, "tradeNumber").get_attribute("innerText")
            with open('lot_numbers.txt', 'r') as r:
                if lotNum in r.read():
                    driver.execute_script("document.getElementsByClassName('card')[0].remove()")
                else:
                    with open('lot_numbers.txt', 'a') as f:
                        f.write(lotNum)
                        if driver.find_element(By.ID, "applicationSendButton"):
                            driver.find_element(By.ID, "applicationSendButton").click()
                        break
        else:
            refresh_btn.click()
            time.sleep(1)

    # time.sleep(5) # Ожидание прогрузки страницы торга

    while True:
        if driver.find_elements(By.CLASS_NAME, "fixed-filling"):
            driver.execute_script("document.getElementsByClassName('fixed-filling')[0].remove()")
            break
        else:
            time.sleep(1)

    if driver.find_elements(By.CSS_SELECTOR, ".load-from-storage-btn"):
            loadDoc = driver.find_elements(By.CSS_SELECTOR, ".load-from-storage-btn")[0]
            loadDoc.click()
            while True:
                if driver.find_elements(By.CSS_SELECTOR, ".add-document-btn"):
                    addDoc = driver.find_elements(By.CSS_SELECTOR, ".add-document-btn")[0]
                    addDoc.click()
                    docName = driver.find_element(By.ID, "documentEditableNameInput-0")
                    docName.send_keys('Документы')
                    break
                else:
                    time.sleep(1)

    price = driver.find_element(By.ID, "lotItemPriceInput-0")

    for i in range(20):
        price.send_keys(Keys.BACKSPACE)

    price.send_keys("0,01")

    while True:
        if driver.find_elements(By.CSS_SELECTOR, ".tax"):
            driver.find_elements(By.CSS_SELECTOR, ".tax")[0].click()
            break
        else:
            time.sleep(1)

    if driver.find_elements(By.CLASS_NAME, "select-tru__icon"):
        tru = driver.find_elements(By.CLASS_NAME, "select-tru__icon")
        tru[0].click()

        truOption = driver.find_elements(By.CLASS_NAME, "tru-description-modal__action")
        truOption[1].click()

        time.sleep(2)
        while True:
            if driver.find_element(By.ID, "add-offer"):
                truBtn = driver.find_element(By.ID, "add-offer")
                truBtn.click()
                time.sleep(1)
                break
            else:
                time.sleep(1)
    else:
        time.sleep(1)

    send = driver.find_elements(By.TAG_NAME, "button")
    driver.execute_script("window.scrollTo(0, 10000)")
    send[3].click()

    while True:
        if driver.find_elements(By.CLASS_NAME, "c-btn--secondary"):
            driver.find_elements(By.CLASS_NAME, "c-btn--secondary")[1].click()
            break
        else:
            time.sleep(1)

    time.sleep(2)

    #if driver.find_element(By.ID, "signButton"):
     #   driver.find_element(By.ID, "signButton").click()

    kb = Controller()

    #if driver.find_elements(By.):
    #    kb.press(Key.tab)
    #    kb.release(Key.tab)
    #    kb.press(Key.enter)
    #    kb.release(Key.enter)

    #if driver.find_element(By.ID, ""):
    #    if driver.find_element(By.ID,""):
    #        signature = driver.find_element(By.ID, "")
    #        if "ФИТТБЕР" in signature.get_attribute("innerText"):
    #            signature.click()
    #        else:
    #            driver.execute_script("--remove--")

    time.sleep(10000)

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
    #window()
    main()
