 # Given a string regarding data about what kind of furniture you want to see you will get a list of dictionaries with information about the furnitures returned
 # 1 - Access website and make a query for the string
 # 2 - Get data from the search result to build the furniture list
    # 2.1 - Find the elements with info about each furniture
    # 2.2 - Build the dictionary for each furniture
 # 3 - Return the data in a list of dictionaries with furniture info
import requests
from bs4 import BeautifulSoup
# import re
from products import Product, ProductDatabase

class ParsedPage:
    parsed_html = None

    def __init__(self, parsed_html):
        parsed_html = parsed_html


def retrieve_furniture_info_list():
    return []


def retrieve_html_parsed_from_url(query: str) -> BeautifulSoup:
    query_with_hifen = query.lower().replace(' ', '-')
    url = f'https://www.americanas.com.br/busca/{query_with_hifen}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ParsedPage.parsed_html = soup
    return soup


def convert_BRL_currency_to_float(currency_value: str) -> float:
    # Value is received like this: '1.498,00'
    float_value = currency_value.replace('.', '/').replace(',', '.').replace('/', '')
    return float(float_value)


def get_info_dict_for_product(item) -> dict:
    ''' Return a dictionary with main information about the product item passed '''

    price_span = item.select('span[class*="PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ"]')
    price_span = price_span[0] if len(price_span) else None
    product_anchor = item.select('a[class*="Link-bwhjk3-2"]')
    product_anchor = product_anchor[0] if len(product_anchor) else None
    image = product_anchor.find('img')
    # price_span_with_a_mais_tag = item.find("span", class_="PriceUI-bwhjk3-11 cmTHwB PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ")
    # price_span_with_a_mais_tag = item.find("span", class_="PriceUI-bwhjk3-11 jtJOff PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ")
    name_h2 = item.find("h2", class_="TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc")

    name = name_h2.get_text() if name_h2 else 'SEM NOME'
    price_str = price_span.get_text() if price_span else 'SEM PRECO'
    link_url = product_anchor.get('href') if product_anchor else 'SEM LINK'
    image_url = image.get('src') if image else 'SEM IMAGEM'

    if price_span:
        # Value is received like this: 'R$ 1.498,00'
        price_str = price_span.get_text() 
        price = convert_BRL_currency_to_float(price_str[3:])
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
    product = Product(info_dict)
    return info_dict


def get_info_list_about_products(parsed_html: BeautifulSoup) -> list:
    ''' Returns a list with all the information about the products from the given parsed html page '''
    grid_items = parsed_html.find_all("div", class_="product-grid-item")
    item = grid_items[0]
    items_list = []
    print(len(grid_items))

    # price_span_regex = re.compile('PriceUI-bwhjk3-11.* PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ')
    for item in grid_items:
        info_dict = get_info_dict_for_product(item)
        items_list.append(info_dict)
    # import pdb; pdb.set_trace()
    return items_list


def store_products_on_json():
    ''' Dumps the ProductDatabase to a json file '''
    import json

    all_products = ProductDatabase.products
    with open('products.json', 'w') as file:
        json.dump([product.__dict__ for product in all_products], file, indent=4)


def get_data_from_json():
    ''' Read JSON file and return its data'''
    import json

    with open('products.json') as data_file:
        data_loaded = json.load(data_file)
    return data_loaded


def populate_products_database_from_json_and_return_list():
    ''' Gets all the data from json file and create Product objects to populate ProrductDatabase '''
    data_loaded = get_data_from_json()
    products_list = []
    for data in data_loaded:
        print(data)
        products_list.append(Product(data))
    return products_list
