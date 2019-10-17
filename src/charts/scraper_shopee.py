import requests


def get_brands(quote, results=100):
    headers = {
        'User-Agent': 'Mozilla/5',
        'Referer': "https://shopee.com.my/search?keyword={}".format(quote)
    }

    url = "https://shopee.com.my/api/v2/search_items/?by=relevancy&keyword={}&limit={}&newest=0&order=desc&page_type=search".format(quote, results)
    r = requests.get(url, headers=headers).json()

    for item in r['items']:
        yield item['brand']


def shopee_dict(quote, results=100):
    """
    returns a dictionary with brands and items per brand
    and also total number of items found
    (this number can be used for testing results)
    """

    brands = {}
    total_items = 0
    for brand in get_brands(quote, results):
        if brand in brands:
            brands[brand] += 1
        else:
            brands[brand] = 1
        total_items += 1
    return brands, total_items


if __name__ == '__main__':
    """
    Scraper for Shopee.vn
    Scrape: share of search of all brands on the top 'X' results for a given quote
    Takes 2 arguments: quote and number of results 
    """
    search_string = 'lipstick'
    # search_string = 'son lì'
    items = 100

    brands_dict, number = shopee_dict(search_string, items)

    print('-' * 35)
    print('Brands:\n' + str(brands_dict))
    print('Total items:', items)
    print('-' * 35)
