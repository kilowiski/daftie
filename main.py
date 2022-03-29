'''
    find ur irish house
'''
import os
import time
import sys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from daftlistings import Daft, Location, SearchType, PropertyType
from dotenv import load_dotenv

def init_driver():
    '''
        webdriver inits etc here
    '''
    #get env variables, create your own .env
    global driver
    global chrome_options
    load_dotenv()
    prev_list = []
    #selenium webdriver config, this is fine no prob
    chrome_options = Options()
    #TURNS OUT IS BECAUSE THE EMAIL IS OUTSIDE OF THE VIEWPORT AAA
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.implicitly_wait(5)

def daft_search():
    '''
        edit here to specify daft search
    '''
    global listings
    daft = Daft()
    daft.set_location(Location.DUBLIN)
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    daft.set_property_type(PropertyType.APARTMENT)
    daft.set_min_price(3000)
    daft.set_max_price(3001)
    listings = daft.search(max_pages=1)

def send_query(url):
    '''
        core of the script bruh, clicks "email agent", fill field + submit
    '''
    #function that opens the page
    driver.get(url)

    #skip the fucking cookie
    try:
        cookie_elem="//button[@class='cc-modal__btn cc-modal__btn--daft']"
        cookiebutton=driver.find_element_by_xpath(cookie_elem)
    except NoSuchElementException:
        print("continue on")
    else:
        cookiebutton.click()
    finally:
        try:
            #click the email agent button
            driver.implicitly_wait(5)
            email_agent_button="//button[@class='NewButton__StyledButton-yem86a-2 fhElqk']"
            button = driver.find_element_by_xpath(email_agent_button)
            ActionChains(driver).move_to_element(button).click(button).perform()

            #NOW FILL UP THE FORM
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//input[@id='keyword1']").send_keys(os.getenv('FULL_NAME'))
            driver.find_element_by_xpath("//input[@id='keyword2']").send_keys(os.getenv('USER_EMAIL'))
            driver.find_element_by_xpath("//input[@id='keyword3']").send_keys(os.getenv('PHONE'))
            driver.find_element_by_xpath("//textarea[@data-testid='textarea']").send_keys(os.getenv('MESSAGE'))


            #THIS BUTTON SUBMITS YOUR QUERY, PLEASE COMMENT OUT IF NOT USING
            driver.find_element_by_xpath("//button[@data-testid='submit-button']").click()
        except StaleElementReferenceException:
            print("retry again")
            driver.implicitly_wait(30)
            driver.find_element_by_xpath("//input[@id='keyword1']").send_keys(os.getenv('FULL_NAME'))
            driver.find_element_by_xpath("//input[@id='keyword2']").send_keys(os.getenv('USER_EMAIL'))
            driver.find_element_by_xpath("//input[@id='keyword3']").send_keys(os.getenv('PHONE'))
            driver.find_element_by_xpath("//textarea[@data-testid='textarea']").send_keys(os.getenv('MESSAGE'))


            #THIS BUTTON SUBMITS YOUR QUERY, PLEASE COMMENT OUT IF NOT USING
            driver.find_element_by_xpath("//button[@data-testid='submit-button']").click()
        finally:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "keyword1"))
                )
                element.send_keys(Keys.TAB)
            except StaleElementReferenceException:
                print("retry again")
                driver.implicitly_wait(30)
                element.send_keys(Keys.TAB)
            finally:
                print("we done here")
            time.sleep(10)

def login():
    '''
        login here, please use .env file to input your credentials
    '''
    driver.get("https://www.daft.ie/")
        #skip the fucking cookie
    try:
        cookie_elem="//button[@class='cc-modal__btn cc-modal__btn--daft']"
        cookiebutton=driver.find_element_by_xpath(cookie_elem)
        cookiebutton.click()
        driver.find_element_by_xpath("//li[@data-testid='nav-item-signin']").click()
        driver.find_element_by_xpath("//input[@id='username']").send_keys(os.getenv('USER_EMAIL'))
        driver.find_element_by_xpath("//input[@id='password']").send_keys(os.getenv('PASSWORD'))
        driver.find_element_by_xpath("//*[@class='login__button']").click()
    except NoSuchElementException :
        return
    except ElementNotInteractableException:
        return
    else:
        print("continue on")

def read_list():
    '''
        func that reads stuff
    '''
    path = Path("./prev_list.txt")
    prev_list=[]

    if path.is_file():
        print("there exists the file")
        with open("prev_list.txt", "r") as f:
            reads= f.readlines()
        for x in reads:
            z=x.replace("\n","")
            prev_list.append(z)
    else:
        print("file not created,creating now")
        f = open("prev_list.txt", "a")
    return prev_list

def query_test():
    login()
    for i in range(3):
        print(f"{i} for link : {listings[i].daft_link}")
        send_query(listings[i].daft_link)
        print("==============")

def query_run():
    login()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    previous=read_list()
    intermediate=listings.copy()

    print(len(intermediate))
    for x in listings:
        if x.daft_link in previous:
            print("REMOVING " +x.daft_link)
            for z in intermediate:
                if z.daft_link == x.daft_link:
                    intermediate.remove(z)
        else:
            print("no it isnt")
    print(len(intermediate))

    #finally send queries
    for x in intermediate:
        send_query(x.daft_link)
        print("==============")

    print("copy listings to text")
    f = open("prev_list.txt", "a")
    for x in intermediate:
        f.write(x.daft_link+"\n")
    f.close()

#this is the main loop
while True:
    init_driver()
    daft_search()
    query_run()
    print("OWARIMASHO")
    driver.implicitly_wait(5)
    driver.close()
    print("sleep")
    time.sleep(os.getenv('REFRESH_PERIOD_IN_SECONDS'))
    print("awake")
