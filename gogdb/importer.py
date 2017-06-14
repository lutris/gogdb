from __future__ import print_function
import json
from urllib import urlencode
from collections import defaultdict
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
        params['page'] = page
        response = requests.get(api_endpoint + "?" + urlencode(params))
        store.set_page(page, response.json())


def iter_products():
    store = GOGStore()
    for page in range(1, store.get_page_count() + 1):
        page_results = store.get_page(page)
        for product in page_results['products']:
            yield product


def check_uniqueness():
    seen_ids = defaultdict(list)
    seen_slugs = defaultdict(list)
    for product in iter_products():
        product_id = product['id']
        seen_ids[product_id].append(product['title'])
        seen_slugs[product['slug']].append(product['title'])

    for product_id in seen_ids:
        if len(seen_ids[product_id]) > 1:
            print('Duplicate ids:', ' | '.join(seen_ids[product_id]))

    for slug in seen_slugs:
        if len(seen_slugs[slug]) > 1:
            print('Duplicate slugs:', ' | '.join(seen_slugs[slug]))


def export_db(dest_filename):
    gog_list = []
    for product in iter_products():
        gog_list.append({
            'id': product['id'],
            'title': product['title'],
            'slug': product['slug'],
        })
    with open(dest_filename, 'w') as dest_file:
        json.dump(gog_list, dest_file, indent=2)


if __name__ == '__main__':
    export_db("gogdb.json")
