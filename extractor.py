from typing import Tuple, List
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, element
from products import Product


PATH = 'C:\\Users\\carlo\\Documents\\ESTUDOS\\chromedriver.exe'

class DataRetriever:
    ''' Class that uses multiple PageExtractors to retrieve data queried from different websites '''

    STORES_BASE_URLS = {
        'magazineluiza': 'https://busca.magazineluiza.com.br/busca?q={}',
        'americanas': 'https://www.americanas.com.br/busca/{}',
        'submarino': 'https://www.submarino.com.br/busca/{}',
        'casasbahia': 'https://www.casasbahia.com.br/{}/b',
        'extra': 'https://www.extra.com.br/{}/b'
    }

    def __init__(self, stores_list: List[str] = None):
        if stores_list:
            self.stores_ids_list = stores_list
        else:
            self.stores_ids_list = [*self.STORES_BASE_URLS]

    def query_for(self, query: str) -> List[dict]:
        ''' Returns a list of products dictionaries got from querying each website on DataReceiver's stores_ids_list '''
        # Execute this query in as many websites there are in STORES_BASE_URLS
        # websites_to_query = [*PageExtractor.STORES_BASE_URLS]
        websites_to_query = self.stores_ids_list
        objects_retrieved = []
        # import pdb; pdb.set_trace()
        for website in websites_to_query:
            website_objects = PageExtractor(website).query_webdriver(query)
            print(len(website_objects))
            objects_retrieved = objects_retrieved + website_objects
        return objects_retrieved

    @classmethod
    def store_products_on_json(cls, products, file_name):
        ''' Dumps the list of products to a json file with file_name '''
        import json

        with open(file_name, 'w') as file:
            json.dump([product.__dict__ for product in products], file, indent=4)

    @classmethod
    def get_products_from_json(cls, file_name: str) -> List[Product]:
        ''' Return a list of products extracted from json file with file_name '''
        import json

        products = []
        with open(file_name) as data_file:
            data_loaded = json.load(data_file)
            for data in data_loaded:
                products.append(Product(data))

        return products


class PageExtractor:
    '''Class used to make it easier to extract data from previously known e-commerce website'''

    STORES_BASE_URLS = {
        'magazineluiza': 'https://busca.magazineluiza.com.br/busca?q={}',
        'americanas': 'https://www.americanas.com.br/busca/{}',
        'submarino': 'https://www.submarino.com.br/busca/{}',
        'casasbahia': 'https://www.casasbahia.com.br/{}/b',
        'extra': 'https://www.extra.com.br/{}/b'
    }

    STORES_PRODUCTS_PATHS = {
        'magazineluiza': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('li', 'nm-product-item'),
            'price': ('div', 'nm-price-container'),
            'name': ('h2', 'nm-product-name'),
            'link': ('a', 'nm-product-item-container'),
            'image': ('img', 'nm-product-img')
        },
        'magazineluiza2': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('li', 'product'),
            'price': ('span', 'price'),
            'name': ('h3', 'productTitle'),
            'link': ('a', 'product-li'),
            'image': ('img', 'product-image')
        },
        'americanas': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('div', 'product-grid-item'),
            'price': ('span', 'PriceUI'),
            'name': ('h2', 'TitleUI'),
            'link': ('a', 'Link'),
            # 'image': ('img', 'nm-product-img'),
            'image': ('img', 'ImageUI')
        },
        'submarino': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('div', 'product-grid-item'),
            'price': ('span', 'PriceUI'),
            'name': ('h2', 'TitleUI'),
            'link': ('a', 'Link'),
            # 'image': ('img', 'nm-product-img'),
            'image': ('img', 'ImageUI')
        },
         'casasbahia': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('li', 'ProductCard__Wrapper'),
            'price': ('span', 'ProductPrice__PriceValue'),
            'name': ('p', 'ProductCard__Title'),
            'link': ('a', None),
            # 'image': ('img', 'nm-product-img'),
            'image': ('img', 'LazyLoadImg')
        },
        'extra': {
            'search_field_id': 'inpHeaderSearch',
            'items': ('li', 'ProductCard__Wrapper'),
            'price': ('span', 'ProductPrice__PriceValue'),
            'name': ('p', 'ProductCard__Title'),
            'link': ('a', None),
            # 'image': ('img', 'nm-product-img'),
            'image': ('img', 'LazyLoadImg')
        }
    }

    # Will store the BeautifulSoup parsed from the search query when calling retrieve_html_parsed_from_query
    parsed_html = None

    def __init__(self, store_id):
        self.store_id = store_id

    def query_webdriver(self, query: str) -> List[dict]:
        ''' Returns list of products dictionaries got from the parsed html of the page.
            Uses the selenium driver to load the PageExtractor website after checking until it located a checkpoint element and then BeautifulSoup it and get_info_list_about_products'''
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        driver = webdriver.Chrome(PATH)
        driver.get(self.get_search_url(query))
        # search = driver.find_element_by_id('inpHeaderSearch')
        # search.send_keys(query + Keys.RETURN)

        if 'magazineluiza' in self.store_id:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "productShowCaseContent"))
                )
                # Stores the id as magazineluiza2 for the PageExtractor know that it'll need to look for especific tags related to it
                self.store_id = 'magazineluiza2'
                print('FOI NO PRIMEIRO')
            except Exception:
                print('DEU ERRO NO PRIMEIRO')
                try:
                    page = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".neemu-products-container.nm-view-type-grid.five-products.priceapi-finish"))
                    )
                    # Stores the id as magazineluiza for the PageExtractor know that it'll need to look for especific tags related to it
                    self.store_id = 'magazineluiza'
                    print('FOI NO SEGUNDO')
                except Exception:
                    print('DEU ERRO NO SEGUNDO')
                    try:
                        page = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "main-title"))
                        )
                    except Exception:
                        import pdb; pdb.set_trace()
                        driver.quit()
            finally:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                products = self.get_info_list_about_products(soup)
                return products
        elif 'americanas' in self.store_id or 'submarino' in self.store_id:
            try:
                page = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".row.product-grid.no-gutters.main-grid"))
                )
                print('FOI NO PRIMEIRO')
            except Exception:
                print('DEU ERRO NO PRIMEIRO')
                import pdb; pdb.set_trace()
                driver.quit()
            finally:
                # In these websites the images are loaded as we scroll down the page
                # Then we had to do this to load the images as we scrollIntoView and retrieve images loaded instead of empty img tag
                all_items = driver.find_elements_by_class_name('product-grid-item')
                iter_idx = 0
                while iter_idx < len(all_items):
                    driver.execute_script("arguments[0].scrollIntoView()", all_items[iter_idx])
                    iter_idx += 1
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                products = self.get_info_list_about_products(soup)
                return products
        elif 'casasbahia' in self.store_id or 'extra' in self.store_id:
            try:
                page = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".ProductsGrid__ProductsGridWrapper-yqpqna-0.joXYON"))
                )
                print('FOI NO SEGUNDO')
            except Exception:
                print('DEU ERRO NO SEGUNDO')
                import pdb; pdb.set_trace()
                driver.quit()
            finally:
                # import pdb; pdb.set_trace()
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                products = self.get_info_list_about_products(soup)
                return products
    
    def get_tag_and_class_for_info(self, item_to_be_extracted: str) -> Tuple[str,str]:
        ''' Returns a tuple with html tag and css class the item_to_be_extracted refers to '''
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
        ''' Returns the search url for the PageExtractor website according to STORES_BASE_URLS and query word of each site'''
        func_dict = {
            'magazineluiza': lambda query: query.lower().replace(' ', '%20'),
            'americanas': lambda query: query.lower().replace(' ', '-'),
            'submarino': lambda query: query.lower().replace(' ', '-'),
            'casasbahia': lambda query: query.lower().replace(' ', '-'),
            'extra': lambda query: query.lower().replace(' ', '-')
        }
        parsed_query = func_dict[self.store_id](query)
        return self.STORES_BASE_URLS[self.store_id].format(parsed_query)
    
    def retrieve_html_parsed_from_query(self, query: str) -> BeautifulSoup:
        ''' Retrieve the first page of the query searched on the e-commerce website parsed to BeautifulSoup object
        and save it to the parsed_html instance variable '''
        url = self.get_search_url(query)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Saving it to the parsed_html variable
        self.parsed_html = soup
        return soup
    
    def get_info_dict_for_product(self, item) -> dict:
        ''' Return a dictionary with main information about the product item passed '''
        # image = product_anchor.find('img')
        img_tag, img_class = self.get_tag_and_class_for_info('image')
        # image = item.find(img_tag, class_=img_class)
        regex = re.compile('.*'+img_class+'.*')
        image = item.find(img_tag, { 'class': regex })
        # if not image:
        #     import pdb; pdb.set_trace()

        name_tag, name_class = self.get_tag_and_class_for_info('name')
        regex = re.compile('.*'+name_class+'.*')
        name_h2 = item.find(name_tag, { 'class': regex })

        price_tag, price_class = self.get_tag_and_class_for_info('price')
        regex = re.compile('.*'+price_class+'.*')
        price_str = item.find(price_tag, { 'class': regex })

        name = name_h2.get_text().strip() if name_h2 else 'SEM NOME'
        # price_str = price_span.get_text() if price_span else 'SEM PRECO'
        image_url = image.get('src') if image else 'SEM IMAGEM'

        link_tag, link_class = self.get_tag_and_class_for_info('link')
        # If there's no class associated then we look for links with the item's title as item's name. All websites are like this
        if link_class:
            # link = item.find(link_tag, class_=link_class)
            regex = re.compile('.*'+link_class+'.*')
            link = item.find(link_tag, { 'class': regex })
        else:
            link = item.find('a', {'title':name})
        link_url = link.get('href') if link else 'SEM LINK'

        if price_str:
            # Value is received like this: 'R$ 1.498,00'
            price_str = price_str.get_text() 
            price = PageExtractor.convert_BRL_currency_to_float(price_str)
        else:
            price_str = 'SEM PRECO'
            price = None

        info_dict = {
            'name': name,
            'price_str': price_str,
            'price': price,
            'link': link_url,
            'image_url': image_url,
            'store': self.store_id
        }

        return info_dict

    def get_items_list_from_parsed_html(self, parsed_html: BeautifulSoup) -> element.ResultSet:
        ''' Returns a list with all the items to be extracted from the given parsed html page '''
        tag, html_class = self.get_tag_and_class_for_info('items')
        # grid_items = parsed_html.find_all(tag, class_=html_class)
        regex = re.compile('.*'+html_class+'.*')
        grid_items = parsed_html.find_all(tag, { 'class': regex })
        return grid_items

    def get_info_list_about_products(self, parsed_html: BeautifulSoup) -> List[dict]:
        ''' Returns a list with all the information about the products from the given parsed html page '''
        grid_items = self.get_items_list_from_parsed_html(parsed_html)
        items_list = []
        print(len(grid_items))
        # import pdb; pdb.set_trace()

        for item in grid_items:
            info_dict = self.get_info_dict_for_product(item)
            items_list.append(info_dict)
        return items_list
    
    @staticmethod
    def convert_BRL_currency_to_float(currency_value: str) -> float:
        ''' Returns float value of the price after handling the string '''
        # Value is received like this: 'R$ 1.498,00' 'R$ 538,90 à vista' 'Desconto de R$ 1,90'
        currency_value = currency_value.strip().split('R$')[1]
        float_value = currency_value.strip().replace('.', '/').replace(',', '.').replace('/', '')
        # It can also come as '3480.00 à vista'
        if 'à vista' in float_value:
            float_value = float_value.split(' à vista')[0]
        return float(float_value)

    def retrieve_products_from_query(self, query: str) -> list:
        ''' Returns a list of Product objects from the extracted data got when searching for the given query in the instance e-commerce website '''
        parsed_html = self.retrieve_html_parsed_from_query(query)
        items_dicts_list = self.get_info_list_about_products(parsed_html)

        products = [Product(item_attrs) for item_attrs in items_dicts_list]
        return products

    @classmethod
    def store_products_on_json(cls, products, file_name):
        ''' Dumps the list of products to a json file with file_name '''
        import json

        with open(file_name, 'w') as file:
            json.dump([product.__dict__ for product in products], file, indent=4)
