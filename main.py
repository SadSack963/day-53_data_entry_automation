from bs4 import BeautifulSoup
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
from time import sleep

chrome_driver_path = "E:/Python/WebDriver/chromedriver.exe"
firefox_driver_path = "E:/Python/WebDriver/geckodriver.exe"
opera_driver_path = "E:/Python/WebDriver/operadriver.exe"

load_dotenv("E:/Python/EnvironmentVariables/.env")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScHVLX-4qmgXvVSB7nebMtvHCyO5ncn63-y-AES0BM602cIjQ/viewform" \
           "?usp=sf_link"
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState={' \
             '"pagination":{},' \
             '"usersSearchTerm":null,' \
             '"mapBounds":{' \
             '"west":-122.56276167822266,' \
             '"east":-122.30389632177734,' \
             '"south":37.69261345230467,' \
             '"north":37.857877098316834' \
             '},' \
             '"isMapVisible":true,' \
             '"filterState":{' \
             '"fr":{"value":true},' \
             '"fsba":{"value":false},' \
             '"fsbo":{"value":false},' \
             '"nc":{"value":false},' \
             '"cmsn":{"value":false},' \
             '"auc":{"value":false},' \
             '"fore":{"value":false},' \
             '"pmf":{"value":false},' \
             '"pf":{"value":false},' \
             '"mp":{"max":3000},' \
             '"price":{"max":872627},' \
             '"beds":{"min":1}' \
             '},' \
             '"isListVisible":true,' \
             '"mapZoom":12' \
             '}'


class Zillow:
    def __init__(self, browser: str = "chrome"):
        b = browser.lower()
        if b == "chrome":
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        elif b == "firefox":
            self.driver = webdriver.Firefox(executable_path=firefox_driver_path)
        elif b == "opera":
            self.driver = webdriver.Opera(executable_path=opera_driver_path)
        else:
            print(f"Invalid browser \"{browser}\".\nOnly Chrome, Firefox and Opera are configured.")
            exit()
        self.driver.get(ZILLOW_URL)

    def find_elements(self, method: str, specifier: str):
        """
        Find all elements on a web page.

        These are the attributes available for method:
            ID = "id",
            XPATH = "xpath",
            LINK_TEXT = "link text",
            PARTIAL_LINK_TEXT = "partial link text",
            NAME = "name",
            TAG_NAME = "tag name",
            CLASS_NAME = "class name",
            CSS_SELECTOR = "css selector".

        :param method: search method
        :param specifier: search attribute
        :return:  list of elements found
        """
        by = method.lower()
        for _ in range(10):
            try:
                if by == "id":
                    list_elements = self.driver.find_elements_by_id(specifier)
                elif by == "xpath":
                    list_elements = self.driver.find_elements_by_xpath(specifier)
                elif by == "link text":
                    list_elements = self.driver.find_elements_by_link_text(specifier)
                elif by == "partial link text":
                    list_elements = self.driver.find_elements_by_partial_link_text(specifier)
                elif by == "name":
                    list_elements = self.driver.find_elements_by_name(specifier)
                elif by == "tag name":
                    list_elements = self.driver.find_elements_by_tag_name(specifier)
                elif by == "class name":
                    list_elements = self.driver.find_elements_by_class_name(specifier)
                elif by == "css selector":
                    list_elements = self.driver.find_elements_by_css_selector(specifier)
                else:
                    print(f"Invalid search method {by}")
                    exit()
                return list_elements
            except common.exceptions.ElementNotInteractableException:
                print("Element Not Interactable Exception")
            except common.exceptions.NoSuchElementException:
                print("No Such Element Exception")
            finally:
                sleep(1)
        print(f"Unable to find any element by \"{by}\" with \"{specifier}\"")


zillow = Zillow("opera")
