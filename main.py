from time import sleep
import beautifulsoup_zillow as z
import selenium_google_forms as s


# Forms Dashboard: https://docs.google.com/forms/u/0/
# Spreadsheet: https://docs.google.com/spreadsheets/d/1fiWcbadPjHeG84kCJR47IEP16liRuKduja47_CNnbew/edit?resourcekey#gid=119844546

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


def fill_in_form():
    # For each item in the Search Listing
    for listing in range(len(list_prices)):
        # print(f"Filling form with details for listing {listing}")

        # Get a list of form questions
        list_elements = form.find_elements("css selector", "div.freebirdFormviewerComponentsQuestionBaseRoot")
        # Enter details into form
        for index in range(len(list_elements)):
            # Get text contents of element
            string: str = list_elements[index].text
            # Detect which question we are working with
            # The order of questions on the form is accounted for
            if string.startswith("Renting Cost"):
                list_elements[index].find_element_by_tag_name("input").send_keys(list_prices[listing])
                pass
            elif string.startswith("Property Address"):
                list_elements[index].find_element_by_tag_name("input").send_keys(list_addresses[listing])
                pass
            elif string.startswith("Link to Web Page"):
                list_elements[index].find_element_by_tag_name("textarea").send_keys(list_urls[listing])
                pass
            else:
                print("HELP! I'm Lost!")
                exit()
        # Find the submit button
        x = form.find_elements("css selector",
                               "div[role='button'][class*='freebirdFormviewerViewNavigationSubmitButton']")
        x[0].click()

        # Wait for new page to load
        sleep(2)

        # Find anchor tag to "Submit another response"
        x = form.find_elements("link text", "Submit another response")
        x[0].click()

        # Wait for new page to load
        sleep(2)


if __name__ == "__main__":
    # Use BeautifulSoup to retrieve the Zillow web page
    soup = z.read_web_file(file=WEB_FILE, url=ZILLOW_URL)
    # print(f"result = {soup}")

    # Get the HTML for the Search Listings Unordered List
    # Speed up Beautiful Soup by only parsing the parts of the document we need
    search_results = soup.find(name="ul", class_="photo-cards photo-cards_wow photo-cards_short")
    # print(f"search_results = {search_results}\n\n")

    # Create a list of URL links for all the Search Listings.
    list_urls = z.get_search_links(html=search_results)
    # print(f"list_urls = {list_urls}\n\n")
    print(len(list_urls))

    # reate a list of prices for all the Search Listings.
    list_prices = z.get_prices(html=search_results)
    # print(f"list_prices = {list_prices}\n\n")
    print(len(list_prices))

    # Create a list of addresses for all the Search Listings.
    list_addresses = z.get_addresses(html=search_results)
    # print(f"list_addresses = {list_addresses}\n\n")
    print(len(list_prices))

    # # Use selenium to fill in the Google Form "San Francisco Renting"
    # # Load the Google Form web page
    # form = s.Form(url=FORM_URL, browser="opera")
    #
    # # Enter details into Google Form
    # fill_in_form()
    #
    # # Close the browser and terminate the WebDriver
    # form.driver.quit()
