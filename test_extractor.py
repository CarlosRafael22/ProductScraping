import pytest
from bs4 import BeautifulSoup, element
from extractor import PageExtractor, DataRetriever
from products import ProductDatabase, Product


test_store_query_data = [
    ('magazineluiza', 'Cadeira escritorio'),
    # ('americanas', 'Cadeira escritorio'),
    ('submarino', 'Cadeira escritorio'),
]

class TestPageExtractor:
    def test_should_init(self):
        extractor = PageExtractor('magazineluiza')
        assert extractor.store_id == 'magazineluiza'

    @pytest.mark.parametrize("store,item,expected_tuple",[
        ('magazineluiza', 'name', ('h2', 'nm-product-name')),
        ('americanas', 'items', ('div', 'product-grid-item')),
        ('submarino', 'discount', (None, None)),
        ('americanas', 'discount', (None, None)),
    ])
    def test_should_get_tag_and_class_for_info(self, store, item, expected_tuple):
        extractor = PageExtractor(store)
        tag_and_class = extractor.get_tag_and_class_for_info(item)
        assert tag_and_class == expected_tuple
    
    @pytest.mark.parametrize("store,query,expected_url",[
        ('magazineluiza', 'Cadeira escritorio', 'https://busca.magazineluiza.com.br/busca?q=cadeira%20escritorio'),
        ('americanas', 'Cadeira escritorio', 'https://www.americanas.com.br/busca/cadeira-escritorio'),
        ('submarino', 'Cadeira escritorio', 'https://www.submarino.com.br/busca/cadeira-escritorio'),
        ('casasbahia', 'Cadeira escritorio', 'https://www.casasbahia.com.br/cadeira-escritorio/b'),
    ])
    def test_should_get_search_url(self, store, query, expected_url):
        extractor = PageExtractor(store)
        assert extractor.get_search_url(query) == expected_url

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_retrieve_html_parsed_from_query(self, store, query):
        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        assert type(parsed_html) == BeautifulSoup
        assert extractor.parsed_html == parsed_html

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_get_items_list_from_parsed_html(self, store, query):
        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        parsed_list = extractor.get_items_list_from_parsed_html(parsed_html)
        assert type(parsed_list) == element.ResultSet
        assert type(parsed_list[0]) == element.Tag

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_get_info_dict_for_product(self, store, query):
        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        parsed_list = extractor.get_items_list_from_parsed_html(parsed_html)
        item = extractor.get_info_dict_for_product(parsed_list[0])
        # import pdb; pdb.set_trace()
        assert type(parsed_list) == element.ResultSet
        assert type(item) == dict
        assert item['name'] is not None
        assert item['link'] is not None

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_get_info_list_about_products(self, store, query):
        # previous_product_total = ProductDatabase.get_products_total()

        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        items_list = extractor.get_info_list_about_products(parsed_html)

        # import pdb; pdb.set_trace()
        assert type(items_list) == list
        # assert len(items_list) == ProductDatabase.get_products_total() - previous_product_total
        # assert type(parsed_list[0]) == BeautifulSoup

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_retrieve_products_from_query(self, store, query):
        ProductDatabase.clear_database()

        extractor = PageExtractor(store)
        products_list = extractor.retrieve_products_from_query(query)

        # import pdb; pdb.set_trace()
        assert type(products_list) == list
        assert len(products_list) == ProductDatabase.get_products_total()
        # assert len(items_list) == ProductDatabase.get_products_total() - previous_product_total
        # assert type(parsed_list[0]) == BeautifulSoup

    @pytest.mark.parametrize("store,query",test_store_query_data)
    def test_should_store_products_on_json(self, store, query):
        import os
        ProductDatabase.clear_database()
        filename = 'test.json'

        extractor = PageExtractor(store)
        products_list = extractor.retrieve_products_from_query(query)
        extractor.store_products_on_json(products_list, filename)

        # import pdb; pdb.set_trace()
        assert os.path.exists(filename) == True
        assert len(products_list) == ProductDatabase.get_products_total()
        # assert len(items_list) == ProductDatabase.get_products_total() - previous_product_total
        # assert type(parsed_list[0]) == BeautifulSoup

    currency_test_data = [
        ('R$ 1.234,78', 1234.78),
        ('R$ 538,90 à vista', 538.90),
        ('R$ 34.890,90 à vista', 34890.90),
        ('Desconto de R$ 1,90', 1.90)
    ]
    @pytest.mark.parametrize("currency_str,expected_float", currency_test_data)
    def test_should_convert_BRL_currency_to_float(self, currency_str, expected_float):
        value = PageExtractor.convert_BRL_currency_to_float(currency_str)
        assert value == expected_float

    def test_should_open_webdriver(self):
        import os
        import pandas as pd
        from products import Product
        ProductDatabase.clear_database()
        filename = 'test.json'

        extractor = PageExtractor('magazineluiza')
        products_list = extractor.query_webdriver("iphone")
        products = [Product(item_attrs) for item_attrs in products_list]
        extractor.store_products_on_json(products, filename)
        # import pdb; pdb.set_trace()
        filtered_products = ProductDatabase.filter(price__gte=3000, price__lt=4000)
        extractor.store_products_on_json(filtered_products, 'test_filtered.json')

        # df = pd.DataFrame({
        #     'name': [prod.name for prod in filtered_products],
        #     'price': [prod.price for prod in filtered_products]
        # })

        # import pdb; pdb.set_trace()
        assert os.path.exists(filename) == True
        assert len(products_list) == ProductDatabase.get_products_total()


class TestDataRetriever:
    def test_should_query_for(self):
        products_dicts = DataRetriever.query_for('iphone')
        # import pdb; pdb.set_trace()
        products = [Product(item_attrs) for item_attrs in products_dicts]
        DataRetriever.store_products_on_json(products, 'test.json')
        # import pdb; pdb.set_trace()
        filtered_products = ProductDatabase.filter(price__gte=3000, price__lt=4000)
        DataRetriever.store_products_on_json(filtered_products, 'test_filtered.json')
        assert type(products_dicts) == list
        assert type(products_dicts[0]) == dict
    
    def test_should_get_products_from_json(self):
        ProductDatabase.clear_database()
        products = DataRetriever.get_products_from_json('test.json')
        assert len(products) == len(ProductDatabase.products)
        assert products[0] == ProductDatabase.products[0]