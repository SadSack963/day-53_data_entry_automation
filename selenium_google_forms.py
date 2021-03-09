from selenium import webdriver, common
import os
from dotenv import load_dotenv  # pip install python-dotenv
from time import sleep


# Use Selenium to fill in the form you created

class Form:
    def __init__(self, url: str, browser: str = "chrome"):
        """
        Create a selenium object.\n
        Open the requested URL with the requested browser.

        :param url: the web page URL we want to use
        :param browser: the browser to open the web page in (Optional. Default: chrome)
        """
        browser = browser.lower()
        # Declare variables
        self.chrome_driver_path = self.firefox_driver_path = self.opera_driver_path = ""

        # Get the path to the WebDriver and environment variables
        #   depending upon the operating system
        self.get_os_path()
        self.driver = self.get_driver(browser)
        self.driver.get(url)

    def get_os_path(self):
        # Detect Operating System and set paths to local files
        import platform
        if platform.system() == "Windows":
            self.chrome_driver_path = "E:/Python/WebDriver/chromedriver.exe"
            self.firefox_driver_path = "E:/Python/WebDriver/geckodriver.exe"
            self.opera_driver_path = "E:/Python/WebDriver/operadriver.exe"
            load_dotenv("E:/Python/EnvironmentVariables/.env")
        elif platform.system() == "Linux":
            # (Set WebDriver file permissions to 755)
            # -rwxr-xr-x 1 john john 11755976 Jan 27 03:32 chromedriver
            # -rwxr-xr-x 1 john john  7965656 Jan 14 08:51 geckodriver
            # -rwxr-xr-x 1 john john 14990832 Feb  3 10:29 operadriver
            self.chrome_driver_path = "/home/john/Development/Python/WebDriver/chromedriver"
            self.firefox_driver_path = "/home/john/Development/Python//WebDriver/geckodriver"
            self.opera_driver_path = "/home/john/Development/Python/WebDriver/operadriver"
            load_dotenv("/media/sf_Python/EnvironmentVariables/.env")
        else:
            print("OS not supported!")
            exit()

    def get_driver(self, b):
        if b == "chrome":
            driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        elif b == "firefox":
            driver = webdriver.Firefox(executable_path=self.firefox_driver_path)
        elif b == "opera":
            driver = webdriver.Opera(executable_path=self.opera_driver_path)
        else:
            print(f"Invalid browser \"{b}\".\nOnly Chrome, Firefox and Opera are configured.")
            exit()
        return driver

    def find_elements(self, method: str, specifier: str):
        """
        Find all elements on a web page.

        These are the attributes available for method:
            ID = "id",\n
            XPATH = "xpath",\n
            LINK_TEXT = "link text",\n
            PARTIAL_LINK_TEXT = "partial link text",\n
            NAME = "name",\n
            TAG_NAME = "tag name",\n
            CLASS_NAME = "class name",\n
            CSS_SELECTOR = "css selector".\n

        :param method: search method
        :param specifier: search attribute
        :return:  list of elements found
        """
        by = method.lower()
        list_elements = []
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


