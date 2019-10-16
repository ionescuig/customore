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


if __name__ == '__main__':
    search = "lipstick"
    items = 100

    brands = {}
    total_items = 0
    for brand in get_brands(search, items):
        if brand in brands:
            brands[brand] += 1
        else:
            brands[brand] = 1
        total_items += 1

    print('-' * 35)
    print('Brands:\n' + str(brands))
    print('Total items:', total_items)
    print('-' * 35)
