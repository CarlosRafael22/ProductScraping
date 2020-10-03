import pytest
from extractor import PageExtractor

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