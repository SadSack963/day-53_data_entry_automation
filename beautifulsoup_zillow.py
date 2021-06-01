from bs4 import BeautifulSoup


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

    # NOTE: This may not work because of anti-robot Captcha
    # pip install requests-html
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


def get_search_links(html):
    """
    Search the HTML for anchor tags with tabindex="0".\n
    Form these into a list.

    :param html: the html section to be examined
    :return: list of URLs
    """
    list = [a["href"] for a in html.find_all("a", tabindex="0")]
    # print(f"list_links = {list_links}\n\n")

    # Some links are broken,i.e. an apartment block with multiple listings...
    # Each apartment then has it's own "homedetails" on the destination page.
    #   e.g. '/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    #        should be 'https://www.zillow.com/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    for index in range(len(list)):
        if not list[index].startswith("http"):
            list[index] = 'https://www.zillow.com' + list[index]
            # print(f"Corrected Link = {list_links[index]}\n\n")
    # print(f"list_links = {list_links}\n\n")
    return list


def get_addresses(html):
    """
    Search the HTML for address tags with specific class.\n
    Form these into a list.

    :param html: the html section to be examined
    :return: list of addresses
    """
    list = [a.text for a in html.find_all("address", class_="list-card-addr")]
    # print(f"list_addresses = {list_addresses}\n\n")

    return list


def get_prices(html):
    """
    Search the HTML for div tags with specific class.\n
    Form these into a list.

    :param html: the html section to be examined
    :return: list of prices
    """
    list = [a.text for a in html.find_all("div", class_="list-card-price")]
    # print(f"list_cost = {list_cost}\n\n")

    return list
