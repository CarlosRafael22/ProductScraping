
 # Given a string regarding data about what kind of furniture you want to see you will get a list of dictionaries with information about the furnitures returned
 # 1 - Access website and make a query for the string
 # 2 - Get data from the search result to build the furniture list
    # 2.1 - Find the elements with info about each furniture
    # 2.2 - Build the dictionary for each furniture
 # 3 - Return the data in a list of dictionaries with furniture info
import requests
from bs4 import BeautifulSoup


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


def get_info_dictionary_about_furniture(parsed_html: BeautifulSoup) -> dict:
    grid_items = parsed_html.find_all("div", class_="product-grid-item")
    item = grid_items[0]
    items_list = []
    # for item in grid_items:
    price_span = item.find("span", class_="PriceUI-bwhjk3-11 cmTHwB PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ")
    name_h2 = item.find("h2", class_="TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc")
    info_dict = {
        'name': name_h2.get_text(),
        'price_str': price_span.get_text()
    }
    # import pdb; pdb.set_trace()
    return info_dict


class TestFurnitureRetrieval:
    def test_should_retrieve_furniture_info_list(self):
        furniture_list = retrieve_furniture_info_list()
        assert type(furniture_list) == list
    
    def test_should_retrieve_html_parsed_from_url(self):
        html_parsed = retrieve_html_parsed_from_url('Cadeira gamer')
        assert html_parsed is not None
        assert type(html_parsed) == BeautifulSoup
    
    def test_should_get_info_dictionary_about_furniture(self):
        parsed_html = ParsedPage.parsed_html
        dictionary = get_info_dictionary_about_furniture(parsed_html)
        import pdb; pdb.set_trace()
        assert type(dictionary) == dict


