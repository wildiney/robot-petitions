import os
import time
import sys
import getpass

from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

load_dotenv('./.env')


class Purchases:
    def __init__(self, debug=True):
        self.articles = {
            1: ["SER_13.02", "Fonografia ou gravação de sons, inclusiv"],
            2: ["SER_17.01", "Assessoria e Consultoria dde qualquer natureza"],
            3: ["SER_17.02", "Datilografia, digitação, estenografia, e"],
            4: ["9020800000", "Tarjeta de Visita (Caja 100)"],
            5: ["9070300100", "Artigos gerais de escritório"],
            6: ["OUTROS_16", "Outros"],
        }
        self.user = input("USER: ") or os.environ.get('USER')
        self.password = getpass.getpass(
            "PASSWORD: ") or os.environ.get('PASSWORD')

        print("\r")
        print("Select the number equivalent to your center cost")
        print("1) 7373|100031_1")
        print("2) 7351|100031_2012")
        print("3) 7373|20IM03_1 - AAPP")
        cc_selected = input("Centro de custo: ")
        if (cc_selected == "1"):
            self.cost_center_number = "7373|100031_1"
            print(self.cost_center_number)
        elif(cc_selected == "2"):
            self.cost_center_number = "7351|100031_2012"
            print(self.cost_center_number)
        elif(cc_selected == "3"):
            self.cost_center_number = "7373|20IM03_1"
            print(self.cost_center_number)
        else:
            raise TypeError("Invalid number")

        print("\r")
        print("Select the kind of basket")
        print("1) Material *")
        print("2) Services")
        kb_selected = input("Tipo de cesta: ")
        if(kb_selected == "1"):
            self.kind_of_basket = "material"
            print(self.kind_of_basket)
        elif (kb_selected == "2"):
            self.kind_of_basket = "services"
            print(self.kind_of_basket)
        else:
            raise TypeError("Invalid number")

        print("\r")
        print("Select or digit the article number")
        for k, v in self.articles.items():
            print(k, v[0], v[1])

        print("\r")
        an_selected = input("Número de artigo: ")
        if(len(an_selected) > 1):
            self.article_code = an_selected
        else:
            self.article_code = self.articles.get(int(an_selected))[0]

        print("\r")
        self.hours_amount = input("Horas / Parcelas: ") or "1"

        print("\r")
        self.value = input("Valor total: R$ ") or "1,00"

        print("\r")
        self.date = input("Date [dd.mm.aaaa]: ") or datetime.strftime(datetime.strptime(str(date.today()), "%Y-%m-%d")+timedelta(days=7), '%Y.%m.%d')
        # date.today().strftime('%d.%m.%Y')
        self.address_code = "0001458987"
        self.center = "7373 - INDRA COMPANY BRASIL TECNOLOGI"

        print("\r")
        print(("").ljust(80, "="))
        print(
            self.cost_center_number, "|",
            self.kind_of_basket, "|",
            self.article_code, "|",
            self.hours_amount, "|",
            self.value)
        print(("").ljust(80, "="))

        print("\r")
        self.debug = debug
        self.browser = None
        self.executable_path = os.environ.get("CHROME_DRIVER_PATH")

    def timer(self, timer, message="Loading data: "):
        for t in range(timer):
            sys.stdout.write('\r')
            sys.stdout.flush()
            sys.stdout.write((str(message) + str(timer - t) +
                              ' seconds').ljust(50) + '\r')
            time.sleep(1)

    def msg(self, msg):
        print((msg + " ").ljust(80, "="))

    def launch(self):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1024x768")
        print("\r")
        print(("").ljust(80, "="))
        self.msg("Acessando página inicial")
        self.browser = webdriver.Chrome(
            options=options, executable_path=self.executable_path)
        self.browser.implicitly_wait(60)
        self.browser.get(os.environ.get("SITE_ENTRY"))
        # self.browser.minimize_window()

    def login(self):
        self.msg("Logando no sistema")
        current_url = self.browser.current_url
        self.msg("Acessing "+current_url)
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "login")))
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "passwd")))
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "nsg-x1-logon-button")))
        self.browser.find_element_by_id("login").send_keys(self.user)
        self.browser.find_element_by_id("passwd").send_keys(self.password)
        self.browser.find_element_by_id("nsg-x1-logon-button").click()
        WebDriverWait(self.browser, 50).until(EC.url_changes(current_url))

    def access_purchasing(self):
        self.msg("Acessando página de Compras")
        current_url = self.browser.current_url
        self.browser.get("https://apps.indraweb.net/prelogon.jsp?app=PETCOMPR")
        WebDriverWait(self.browser, 30).until(EC.url_changes(current_url))

    def create_and_show_purchasing(self):
        self.msg("Acessando o Menu Petições de compra")
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "0L2N1")))
        self.browser.find_element_by_id('0L2N1').click()

    def create_purchasing(self):
        self.msg("Acessando iframe")
        self.browser.switch_to.frame('contentAreaFrame')

        self.msg("Acessando menu criar nova compra")
        self.browser.find_element_by_xpath("""/html/body/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr[1]/td[2]/a""").click()

        self.timer(5)
        self.msg("Alterando a janela ativa")
        self.browser.switch_to.window(self.browser.window_handles[1])

        self.msg("Acessando iframe")
        self.browser.switch_to.frame('contentAreaFrame')
        self.browser.switch_to.frame('Compras')

    def access_basket_options(self):
        self.msg("Acessando iframe segundo nível")
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD8D-exp")))
        self.browser.find_element_by_id('WD8D-exp').click()

    def create_material_basket(self):
        if(self.kind_of_basket == "material"):
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD96")))
            self.browser.find_element_by_id("WD96").click()
            self.access_top_frame()

    def create_service_basket(self):
        if(self.kind_of_basket == "services"):
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD9A")))
            self.browser.find_element_by_id("WD9A").click()
            self.access_top_frame()

    def access_top_frame(self):
        self.timer(5)
        self.msg("Acessando janela modal")
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.timer(5)
        self.browser.switch_to.frame('URLSPW-0')

    def cost_center(self):
        self.browser.find_element_by_id('WD0132').send_keys(self.cost_center_number)
        if (self.kind_of_basket == "material"):
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD014B")))
            self.browser.find_element_by_id('WD014B').click()
        else:
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD0146")))
            self.browser.find_element_by_id('WD0146').click()

    def article(self):
        self.timer(5)
        if (self.kind_of_basket == "material"):
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD02E7")))
            self.browser.find_element_by_id('WD02E7').send_keys(self.article_code)
            self.browser.find_element_by_id('WD014B').click()
        else:
            WebDriverWait(self.browser, 50).until(EC.presence_of_element_located((By.ID, "WD01DB")))
            self.browser.find_element_by_id('WD01DB').send_keys(self.article_code)
            self.browser.find_element_by_id('WD0146').click()

    def material_form(self):
        self.timer(5)

        # QTD/HORA
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/span/input")))
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").clear()
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").send_keys(self.hours_amount)

        # CENTRO
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[4]/td[2]/span/span")))
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[1]/div/div/table/tbody/tr[4]/td[2]/span/span""").click()

        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[6]/div/div/div")))
        self.browser.find_element_by_xpath(
            """/html/body/div[6]/div/div/div""").click()

        self.timer(3)

        # VALOR
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[3]/td[2]/div/div/table/tbody/tr/td[1]/span/input")))
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[3]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").clear()
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[3]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").send_keys(self.value)

        # DATA
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[5]/td[2]/span/input")))
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[5]/td[2]/span/input""").clear()
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[5]/td[2]/span/input""").send_keys(self.date)

        # ENDEREÇO
        WebDriverWait(self.browser, 50).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[7]/td[2]/div/div/table/tbody/tr/td[1]/span/input")))
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[7]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").clear()
        self.browser.find_element_by_xpath(
            """/html/body/table/tbody/tr/td/div/div[1]/div[1]/div/div[3]/table/tbody/tr/td/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[6]/td/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[7]/td[2]/div/div/table/tbody/tr/td[1]/span/input""").send_keys(self.address_code)

        self.browser.find_element_by_id("WD014B").click()


pc = Purchases()
pc.launch()
pc.login()
if pc.kind_of_basket == "services":
    sys.exit("No... you can't")
pc.access_purchasing()
pc.create_and_show_purchasing()
pc.create_purchasing()
pc.access_basket_options()
if pc.kind_of_basket == "material":
    pc.create_material_basket()
    pc.cost_center()
    pc.article()
    pc.material_form()
