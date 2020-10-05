from typing import Tuple
import requests
from bs4 import BeautifulSoup, element
from products import Product


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
            'price': ('span', 'PriceUI'),
            'name': ('h2', 'TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc'),
            'link': ('a', 'Link-bwhjk3-2'),
            'image': ('img', 'nm-product-img')
        }
    }

    STORES_BASE_URLS = {
        'magazineluiza': 'https://busca.magazineluiza.com.br/busca?q=',
        'americanas': 'https://www.americanas.com.br/busca/'
    }

    # Will store the BeautifulSoup parsed from the search query when calling retrieve_html_parsed_from_query
    parsed_html = None

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

    def get_search_url(self, query: str) -> str:
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
    
    def retrieve_html_parsed_from_query(self, query: str) -> BeautifulSoup:
        ''' Retrieve the first page of the query searched on the e-commerce website parsed to BeautifulSoup object
        and save it to the parsed_html instance variable '''
        url = self.get_search_url(query)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Saving it to the parsed_html variable
        self.parsed_html = soup
        return soup

    def get_items_list_from_parsed_html(self, parsed_html: BeautifulSoup) -> element.ResultSet:
        ''' Returns a list with all the items to be extracted from the given parsed html page '''
        tag, html_class = self.get_tag_and_class_for_info('items')
        grid_items = parsed_html.find_all(tag, class_=html_class)
        return grid_items

    def get_info_list_about_products(self, parsed_html: BeautifulSoup) -> list:
        ''' Returns a list with all the information about the products from the given parsed html page '''
        grid_items = self.get_items_list_from_parsed_html(parsed_html)
        items_list = []
        print(len(grid_items))

        for item in grid_items:
            info_dict = self.get_info_dict_for_product(item)
            items_list.append(info_dict)
        return items_list
    
    def get_info_dict_for_product(self, item) -> dict:
        ''' Return a dictionary with main information about the product item passed '''
        import re
        # image = product_anchor.find('img')
        img_tag, img_class = self.get_tag_and_class_for_info('image')
        image = item.find(img_tag, class_=img_class)

        name_tag, name_class = self.get_tag_and_class_for_info('name')
        name_h2 = item.find(name_tag, class_=name_class)

        link_tag, link_class = self.get_tag_and_class_for_info('link')
        link = item.find(link_tag, class_=link_class)

        price_tag, price_class = self.get_tag_and_class_for_info('price')
        regex = re.compile('.*'+price_class+'.*')
        price_str = item.find(price_tag, { 'class': regex })
        # name_h2 = item.find("h2", class_="TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc")
        # name_h2 = item.select(name_extractor)
        # name_h2 = name_h2[0] if len(name_h2) else None
        # import pdb; pdb.set_trace()

        name = name_h2.get_text() if name_h2 else 'SEM NOME'
        # price_str = price_span.get_text() if price_span else 'SEM PRECO'
        link_url = link.get('href') if link else 'SEM LINK'
        image_url = image.get('src') if image else 'SEM IMAGEM'

        if price_str:
            # Value is received like this: 'R$ 1.498,00'
            price_str = price_str.get_text() 
            price = PageExtractor.convert_BRL_currency_to_float(price_str[3:])
        else:
            price_str = 'SEM PRECO'
            price = None

        info_dict = {
            'name': name,
            'price_str': price_str,
            'price': price,
            'link': link_url,
            'image_url': image_url
        }
        Product(info_dict)
        return info_dict
    
    @staticmethod
    def convert_BRL_currency_to_float(currency_value: str) -> float:
        # Value is received like this: '1.498,00'
        float_value = currency_value.replace('.', '/').replace(',', '.').replace('/', '')
        return float(float_value)