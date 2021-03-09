from bs4 import BeautifulSoup
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv  # pip install python-dotenv
from time import sleep


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

WEB_FILE = "./data/zillow.html"


# Use Selenium to fill in the form you created

class Form:
    def __init__(self, url, browser: str = "chrome"):
        browser = browser.lower()
        # Declare variables
        self.chrome_driver_path = self.firefox_driver_path = self.opera_driver_path = ""
        # self.driver = webdriver.Chrome()  # Windows error: 'chromedriver' executable needs to be in PATH.

        # Get the path to the WebDriver and environment variables
        #   depending upon the operating system
        self.get_os_path()
        self.get_driver(browser)
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
            self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        elif b == "firefox":
            self.driver = webdriver.Firefox(executable_path=self.firefox_driver_path)
        elif b == "opera":
            self.driver = webdriver.Opera(executable_path=self.opera_driver_path)
        else:
            print(f"Invalid browser \"{b}\".\nOnly Chrome, Firefox and Opera are configured.")
            exit()

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


# Use BeautifulSoup/Requests to scrape all the listings from the Zillow web address

def get_web_page(file, url):
    """
    Retrieve requested web page\n
    Use library render() to execute the page's JavaScript\n
    Save the rendered web page to web file

    :param file: file where web page is saved
    :param url: URL of web page to retrieve
    :return: nothing
    """
    from requests_html import HTMLSession

    # Create an HTML Session object
    session = HTMLSession()
    # Use the object above to connect to needed webpage
    response = session.get(url)
    # Run JavaScript code on webpage
    response.html.render()

    # Save web page to file
    # print("Saving to file")
    with open(file, mode="w", encoding="utf-8") as fp:
        fp.write(response.html.html)


def read_web_file(file, url):
    """
    If web file does not exist, then retrieve web page\n
    Open web file and return a BeautifulSoup object (HTML)

    :param file:  file where web page is saved
    :param url:  URL of web page to retrieve
    :return: HTML soup
    """
    try:
        open(file)
    except FileNotFoundError:
        get_web_page(file, url)
    else:
        pass
    finally:
        # Read the web page from file
        # print("Reading from file")
        with open(file, mode="r", encoding="utf-8") as fp:
            content = fp.read()
        return BeautifulSoup(content, "html.parser")


def get_search_links():
    list_links = [a["href"] for a in search_results.findAll("a", class_="list-card-link list-card-link-top-margin")]
    # print(f"list_links = {list_links}\n\n")

    # Some links are broken
    #   e.g. '/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    #        should be 'https://www.zillow.com/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    for index in range(len(list_links)):
        if not list_links[index].startswith("http"):
            list_links[index] = 'https://www.zillow.com' + list_links[index]
            # print(f"Corrected Link = {list_links[index]}\n\n")
    # print(f"list_links = {list_links}\n\n")
    return list_links


if __name__ == "__main__":
    # Use BeautifulSoup to retrieve the Zillow web page
    soup = read_web_file(file=WEB_FILE, url=ZILLOW_URL)
    # print(f"result = {soup}")

    # Get the HTML for the Search Listings
    search_results = soup.find(name="ul", class_="photo-cards photo-cards_wow photo-cards_short")
    # print(f"search_results = {search_results}\n\n")

    # Create a list of URL links for all the Search Listings.
    get_search_links()

    # TODO Create a list of prices for all the listings you scraped.

    # TODO Create a list of addresses for all the listings you scraped.

    # TODO Use selenium to fill in the Google Form "San Francisco Renting"
    # form = Form(url=FORM_URL, browser="opera")

