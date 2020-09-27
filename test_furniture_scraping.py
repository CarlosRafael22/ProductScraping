
import pytest
from scraping import *

class TestFurnitureRetrieval:
    def test_should_retrieve_furniture_info_list(self):
        furniture_list = retrieve_furniture_info_list()
        assert type(furniture_list) == list
    
    def test_should_retrieve_html_parsed_from_url(self):
        html_parsed = retrieve_html_parsed_from_url('Cadeira gamer')
        assert html_parsed is not None
        assert type(html_parsed) == BeautifulSoup
    
    def test_should_get_info_dictionary_about_furnitures(self):
        parsed_html = ParsedPage.parsed_html
        dictionary = get_info_dictionary_about_furnitures(parsed_html)
        import pdb; pdb.set_trace()
        assert type(dictionary) == list
    
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


