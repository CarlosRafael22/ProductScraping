from typing import Tuple


class PageExtractor:
    '''Class used to make it easier to extract data from previously known e-commerce website'''

    STORES_PRODUCTS_PATHS = {
        'magazineluiza': {
            'items': ('li', 'nm-product-item'),
            'price': ('div', 'nm-price-container'),
            'name': ('h2', 'nm-product-name'),
            'link': ('a', 'nm-product-item-container'),
            'image': ('img', 'nm-product-img')
        },
        'americanas': {
            'items': ('div', 'product-grid-item'),
            'price': ('span', 'PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ'),
            'name': ('h2', 'TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc'),
            'link': ('a', 'Link-bwhjk3-2'),
            'image': ('img', 'nm-product-img')
        }
    }

    STORES_BASE_URLS = {
        'magazineluiza': 'https://busca.magazineluiza.com.br/busca?q=',
        'americanas': 'https://www.americanas.com.br/busca/'
    }

    def __init__(self, store_id):
        self.store_id = store_id
    
    def get_tag_and_class_for_info(self, item_to_be_extracted: str) -> Tuple[str,str]:
        paths = self.STORES_PRODUCTS_PATHS.get(self.store_id, None)
        if not paths:
            return (None, None)
        else:
            tag_and_class = paths.get(item_to_be_extracted, None)
            if not tag_and_class:
                tag_and_class = (None, None)
            return tag_and_class
        # return self.STORES_PRODUCTS_PATHS[self.store_id][item_to_be_extracted]

    def get_search_url(self, query):
        # This way each func is already executed when creating the dict
        # {'magazineluiza': 'cadeira%20escritorio', 'americanas': 'cadeira-escritorio'}
        # func_dict = {
        #     'magazineluiza': query.lower().replace(' ', '%20'),
        #     'americanas': query.lower().replace(' ', '-')
        # }

        # This way it only calls the func when its going to use it
        func_dict = {
            'magazineluiza': lambda query: query.lower().replace(' ', '%20'),
            'americanas': lambda query: query.lower().replace(' ', '-')
        }
        parsed_query = func_dict[self.store_id](query)

        return self.STORES_BASE_URLS[self.store_id]+parsed_query