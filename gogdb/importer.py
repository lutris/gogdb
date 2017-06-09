from urllib import urlencode
import requests

from gogdb.store import GOGStore


def fetch_gog_db(media_type='game', sort='date'):
    store = GOGStore()
    api_endpoint = "https://embed.gog.com/games/ajax/filtered"
    params = {
        'mediaType': media_type,
        'sort': sort,
    }
    page = 1

    response = requests.get(api_endpoint + "?" + urlencode(params))
    results = response.json()
    total_pages = results['totalPages']
    store.set_page(page, results)

    for page in range(2, total_pages + 1):
        response = requests.get(api_endpoint + "?" + urlencode(params))
        store.set_page(page, response.json())


def iter_products_in_pages():
    store = GOGStore()
    for page in range(1, store.get_page_count() + 1):
        page_results = store.get_page(page)
        for product in page_results['products']:
            yield product


if __name__ == '__main__':
    for product in iter_products_in_pages():
        if not product['isGame']:
            print(product['title'])
