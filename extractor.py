from typing import Tuple, List
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, element
from products import Product


PATH = 'C:\\Users\\carlo\\Documents\\ESTUDOS\\chromedriver.exe'


class PageExtractor:
    '''Class used to make it easier to extract data from previously known e-commerce website'''

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
        }
    }

    STORES_BASE_URLS = {
        'magazineluiza': 'https://busca.magazineluiza.com.br/busca?q=',
        'americanas': 'https://www.americanas.com.br/busca/',
        'submarino': 'https://www.submarino.com.br/busca/',
    }

    # Will store the BeautifulSoup parsed from the search query when calling retrieve_html_parsed_from_query
    parsed_html = None

    def __init__(self, store_id):
        self.store_id = store_id

    def query_webdriver(self, query):
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
                page = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "productShowCaseContent"))
                )
                self.store_id = 'magazineluiza2'
                print('FOI NO PRIMEIRO')
            except Exception as excp:
                # import pdb; pdb.set_trace()
                print('DEU ERRO NO PRIMEIRO')
                try:
                    page = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".neemu-products-container.nm-view-type-grid.five-products.priceapi-finish"))
                    )
                    self.store_id = 'magazineluiza'
                    print('FOI NO SEGUNDO')
                except Exception as excp2:
                    # import pdb; pdb.set_trace()
                    print('DEU ERRO NO SEGUNDO')
                    try:
                        page = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "main-title"))
                        )
                    except Exception as excp3:
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
            except Exception as excp:
                import pdb; pdb.set_trace()
                print('DEU ERRO NO PRIMEIRO')
                import pdb; pdb.set_trace()
                driver.quit()
            finally:
                # import pdb; pdb.set_trace()
                all_items = driver.find_elements_by_class_name('product-grid-item')
                iter_idx = 0
                while iter_idx < len(all_items):
                    driver.execute_script("arguments[0].scrollIntoView()", all_items[iter_idx])
                    iter_idx += 1
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                products = self.get_info_list_about_products(soup)
                return products

    # def query_for_all_stores(self, query: str) -> List[Product]:
    #     ''' Uses the query_webdriver method to query all stores listed in PageExtractor and returns all the products '''
    
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
            'americanas': lambda query: query.lower().replace(' ', '-'),
            'submarino': lambda query: query.lower().replace(' ', '-')
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
        # name_h2 = item.find(name_tag, class_=name_class)
        regex = re.compile('.*'+name_class+'.*')
        name_h2 = item.find(name_tag, { 'class': regex })

        link_tag, link_class = self.get_tag_and_class_for_info('link')
        # link = item.find(link_tag, class_=link_class)
        regex = re.compile('.*'+link_class+'.*')
        link = item.find(link_tag, { 'class': regex })

        price_tag, price_class = self.get_tag_and_class_for_info('price')
        regex = re.compile('.*'+price_class+'.*')
        price_str = item.find(price_tag, { 'class': regex })
        # name_h2 = item.find("h2", class_="TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc")
        # name_h2 = item.select(name_extractor)
        # name_h2 = name_h2[0] if len(name_h2) else None
        # import pdb; pdb.set_trace()

        name = name_h2.get_text().strip() if name_h2 else 'SEM NOME'
        # price_str = price_span.get_text() if price_span else 'SEM PRECO'
        link_url = link.get('href') if link else 'SEM LINK'
        image_url = image.get('src') if image else 'SEM IMAGEM'

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
        # Product(info_dict)
        return info_dict

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
    
    @staticmethod
    def convert_BRL_currency_to_float(currency_value: str) -> float:
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
