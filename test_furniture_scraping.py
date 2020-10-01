
import pytest
from scraping import *
from products import Product, ProductDatabase

class TestFurnitureRetrieval:
    def test_should_retrieve_furniture_info_list(self):
        furniture_list = retrieve_furniture_info_list()
        assert type(furniture_list) == list
    
    def test_should_retrieve_html_parsed_from_url(self):
        html_parsed = retrieve_html_parsed_from_url('Cadeira gamer')
        assert html_parsed is not None
        assert type(html_parsed) == BeautifulSoup
    
    def test_should_get_info_list_about_products(self):
        parsed_html = ParsedPage.parsed_html
        products = get_info_list_about_products(parsed_html)
        # import pdb; pdb.set_trace()
        assert type(products) == list

    def test_should_match_get_info_list_about_products_total_with_product_database_total(self):
        parsed_html = ParsedPage.parsed_html
        previous_total = ProductDatabase.get_products_total()
        products = get_info_list_about_products(parsed_html)
        # import pdb; pdb.set_trace()
        assert ProductDatabase.get_products_total() == len(products) + previous_total
    
    currency_test_data = [
        ('1.234,78', 1234.78),
        ('538,90', 538.90),
        ('34.890,90', 34890.90),
        ('1,90', 1.90)
    ]
    @pytest.mark.parametrize("currency_str,expected_float", currency_test_data)
    def test_should_convert_BRL_currency_to_float(self, currency_str, expected_float):
        value = convert_BRL_currency_to_float(currency_str)
        assert value == expected_float
    
    def test_should_get_info_dict_for_product(self):
        parsed_html = ParsedPage.parsed_html
        grid_items = parsed_html.find_all("div", class_="product-grid-item")
        item = grid_items[0]
        # import pdb; pdb.set_trace()
        info_dict = get_info_dict_for_product(item)
        assert type(info_dict) == dict


class TestProductStorage:
    def test_should_store_products_on_json(self):
        import os
        # import pdb; pdb.set_trace()
        store_products_on_json()
        assert os.path.exists('products.json') == True

