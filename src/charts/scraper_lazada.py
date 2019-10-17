import json
import requests
from bs4 import BeautifulSoup
from requests.utils import quote as encode_string


def get_search_url(quote, page=1):
    base_url = "https://www.lazada.vn/catalog/?"
    page = 'page=' + str(page) + '&'
    quote = 'q=' + encode_string(quote)
    complete_url = base_url + page + quote
    return complete_url


def get_soup(url):
    test = False
    while not test:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if 'window.pageData=' in script.text:
                test = True
    return soup


def get_brands(soup, results=40):
    scripts = soup.find_all('script')
    json_obj = None
    for script in scripts:
        if 'window.pageData=' in script.text:
            json_str = script.text

            json_str = json_str.split('window.pageData=')[1]
            json_obj = json.loads(json_str)

            items = 0
            for item in json_obj['mods']['listItems']:
                yield item['brandName']
                items += 1
                if items == results:
                    break


def lazada(quote, results=100):
    """
    yields brands page by page (40 results per page)
    """

    pages = results // 40
    results_remaining = results

    for page in (range(1, pages+2)):
        url = get_search_url(quote, page)
        soup = get_soup(url)
        for item in get_brands(soup, results_remaining):
            yield item
        results_remaining -= 40


def lazada_dict(quote, results=100):
    """
    returns a dictionary with brands and items per brand
    and also total number of items found
    (this number can be used for testing results)
    """

    brands = {}
    total_items = 0
    for brand in lazada(quote, results):
        if brand in brands:
            brands[brand] += 1
        else:
            brands[brand] = 1
        total_items += 1
    return brands, total_items


if __name__ == '__main__':
    """
    Scraper for Lazada.vn
    Scrape: share of search of all brands on the top 'X' results for a given quote
    Takes 2 arguments: quote and number of results 
    """

    # search_string = 'lipstick'
    search_string = 'son lì'
    items = 100

    brands_dict, number = lazada_dict(search_string, items)

    print('-' * 35)
    print('Brands:\n' + str(brands_dict))
    print('Total items:', items)
    print('-' * 35)
