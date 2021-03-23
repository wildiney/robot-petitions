import os
import time
import sys

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

load_dotenv('./.env')

delay = 15

user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
cost_center_number = os.environ.get('COST_CENTER')
kind_of_basket = "material"
article_code = "SER_17.01"
qtd_horas = 1
value = "10,00"
date = "24.04.2021"


def timer(timer, message="Loading data: "):
    for t in range(timer):
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write((str(message) + str(timer - t) +
                          ' seconds').ljust(50) + '\r')
        time.sleep(1)


def wait_for(element):
    wait = WebDriverWait(browser, 30)
    try:
        wait.until(EC.presence_of_element_located((By.ID, element)))
    except TimeoutException as ex:
        print("Exception has been thrown", str(ex))
        browser.quit()


def msg(msg):
    print((msg+" ").ljust(50, "="))


def login():
    msg("Logando no sistema")
    current_url = browser.current_url
    msg("Acessing "+current_url)
    WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.ID, "login")))
    WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.ID, "passwd")))
    WebDriverWait(browser, 50).until(
        EC.presence_of_element_located((By.ID, "nsg-x1-logon-button")))
    browser.find_element_by_id("login").send_keys(user)
    browser.find_element_by_id("passwd").send_keys(password)
    browser.find_element_by_id("nsg-x1-logon-button").click()
    WebDriverWait(browser, 30).until(EC.url_changes(current_url))


def access_purchasing():
    print(("Acessando página de Compras").ljust(50, "="))
    current_url = browser.current_url
    browser.get("https://apps.indraweb.net/prelogon.jsp?app=PETCOMPR")
    WebDriverWait(browser, 30).until(EC.url_changes(current_url))


def create_and_show_purchasing():
    print(("Acessando o Menu Petições de compra").ljust(50, "="))
    browser.find_element_by_id('0L2N1').click()

    # timer(5)
    # WebDriverWait(browser, 30).until(
    #     EC.presence_of_element_located((By.ID, "01L3N0")))
    # browser.find_element_by_id('01L3N0').click()


def create_purchasing():
    print(("Acessando iframe").ljust(50, "="))
    browser.switch_to.frame('contentAreaFrame')

    print(("Acessando menu criar nova compra").ljust(50, "="))
    # browser.find_element_by_css_selector("urLnkDragRelate").click()
    browser.find_element_by_xpath(
        """/html/body/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr[1]/td[2]/a""").click()

    print(("Alterando a janela ativa").ljust(50, "="))
    browser.switch_to.window(browser.window_handles[1])

    print(("Acessando iframe").ljust(50, "="))
    browser.switch_to.frame('contentAreaFrame')
    browser.switch_to.frame('Compras')


def access_basket_options():
    print(("Acessando iframe segundo nível").ljust(50, "="))
    browser.find_element_by_id('WD8D-exp').click()


def create_material_basket():
    browser.find_element_by_id("WD96").click()
    access_top_frame()


def create_service_basket():
    browser.find_element_by_id("WD9A").click()
    access_top_frame()


def access_top_frame():
    timer(5)
    print(("Acessando janela modal").ljust(50, "="))
    # browser.switch_to.parent_frame()
    browser.switch_to.window(browser.window_handles[0])
    browser.switch_to.window(browser.window_handles[1])
    # browser.switch_to.frame(1)
    # browser.switch_to.default_content()
    timer(5)
    browser.switch_to.frame('URLSPW-0')
    # print(browser.page_source)


def cost_center(number):
    browser.find_element_by_id('WD0132').send_keys(number)

    if (kind_of_basket == "material"):
        browser.find_element_by_id('WD014B').click()
    else:
        browser.find_element_by_id('WD0146').click()


def article(code):
    timer(5)
    if (kind_of_basket == "material"):
        browser.find_element_by_id('WD02D3').send_keys(code)
        browser.find_element_by_id('WD014B').click()
    else:
        browser.find_element_by_id('WD01DB').send_keys(code)
        browser.find_element_by_id('WD0146').click()


def material_form():
    browser.find_element_by_id("WD02EC").clear()
    browser.find_element_by_id("WD02EC").send_keys(qtd_horas)

    browser.find_element_by_id("WD0328").clear()
    browser.find_element_by_id("WD0328").send_keys(value)

    browser.find_element_by_id("WD02FE").send_keys(
        "7373 - INDRA COMPANY BRASIL TECNOLOGI")

    browser.find_element_by_id("WD033A").send_keys(date)

    # browser.find_element_by_id("WD014B").click()


options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=740x1080")

print(("Acessando página inicial").ljust(50, "="))
browser = webdriver.Chrome(
    options=options, executable_path=os.environ.get("CHROME_DRIVER_PATH"))
browser.implicitly_wait(60)
browser.get(os.environ.get("SITE_ENTRY"))

login()
access_purchasing()
create_and_show_purchasing()
create_purchasing()
access_basket_options()

if(kind_of_basket == "material"):
    # Criação de cesta de materiais
    create_material_basket()
    cost_center(cost_center_number)
    article(article_code)
    material_form()

if (kind_of_basket == "services"):
    pass
    # Criação de cesta de serviços
    # create_service_basket()
