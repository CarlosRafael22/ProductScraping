import pytest
from bs4 import BeautifulSoup, element
from extractor import PageExtractor
from products import ProductDatabase


class TestPageExtractor:
    def test_should_init(self):
        extractor = PageExtractor('magazineluiza')
        assert extractor.store_id == 'magazineluiza'

    @pytest.mark.parametrize("store,item,expected_tuple",[
        ('magazineluiza', 'name', ('h2', 'nm-product-name')),
        ('americanas', 'items', ('div', 'product-grid-item')),
        ('submarino', 'items', (None, None)),
        ('americanas', 'discount', (None, None)),
    ])
    def test_should_get_tag_and_class_for_info(self, store, item, expected_tuple):
        extractor = PageExtractor(store)
        tag_and_class = extractor.get_tag_and_class_for_info(item)
        assert tag_and_class == expected_tuple
    
    @pytest.mark.parametrize("store,query,expected_url",[
        ('magazineluiza', 'Cadeira escritorio', 'https://busca.magazineluiza.com.br/busca?q=cadeira%20escritorio'),
        ('americanas', 'Cadeira escritorio', 'https://www.americanas.com.br/busca/cadeira-escritorio'),
    ])
    def test_should_get_search_url(self, store, query, expected_url):
        extractor = PageExtractor(store)
        assert extractor.get_search_url(query) == expected_url

    @pytest.mark.parametrize("store,query",[
        ('magazineluiza', 'Cadeira escritorio'),
        ('americanas', 'Cadeira escritorio'),
    ])
    def test_should_retrieve_html_parsed_from_query(self, store, query):
        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        assert type(parsed_html) == BeautifulSoup
        assert extractor.parsed_html == parsed_html

    @pytest.mark.parametrize("store,query",[
        ('magazineluiza', 'Cadeira escritorio'),
        ('americanas', 'Cadeira escritorio'),
    ])
    def test_should_get_items_list_from_parsed_html(self, store, query):
        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        parsed_list = extractor.get_items_list_from_parsed_html(parsed_html)
        assert type(parsed_list) == element.ResultSet
        assert type(parsed_list[0]) == element.Tag

    @pytest.mark.parametrize("store,query",[
        ('magazineluiza', 'Cadeira escritorio'),
        ('americanas', 'Cadeira escritorio'),
    ])
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

    @pytest.mark.parametrize("store,query",[
        # ('magazineluiza', 'Cadeira escritorio'),
        ('americanas', 'Cadeira escritorio'),
    ])
    def test_should_get_info_list_about_products(self, store, query):
        previous_product_total = ProductDatabase.get_products_total()

        extractor = PageExtractor(store)
        parsed_html = extractor.retrieve_html_parsed_from_query(query)
        items_list = extractor.get_info_list_about_products(parsed_html)

        # import pdb; pdb.set_trace()
        assert type(items_list) == list
        assert len(items_list) == ProductDatabase.get_products_total() - previous_product_total
        # assert type(parsed_list[0]) == BeautifulSoup
