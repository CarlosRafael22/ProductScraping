from database import Database
from products import Product
import pytest

class TestDatabase:
    @staticmethod
    def populate_list_for_test():
        test_list = []
        test_list.append(Product({
            'name': 'Product 1',
            'price': 35
        }))
        test_list.append(Product({
            'name': 'Item 1',
            'price': 50
        }))
        test_list.append(Product({
            'name': None,
            'price': 42
        }))
        test_list.append(Product({
            'name': 'Item 2',
            'price': None
        }))
        return test_list

    @pytest.mark.parametrize("lookup,value,expected_name_list", [
        ('price', 35, ['Product 1', 'Item 1', None]),
        ('price', 50, ['Item 1']),
        ('price', 60, []),
    ])
    def test_should_filter_gte(self, lookup, value, expected_name_list):
        test_list = TestDatabase.populate_list_for_test()
        filtered = Database.filter_gte(lookup, value, test_list)
        assert len(filtered) == len(expected_name_list)
        assert [obj.name for obj in filtered] == expected_name_list
    
    @pytest.mark.parametrize("lookup,value,expected_name_list", [
        ('price', 35, ['Product 1']),
        ('name', 'Item 1', ['Item 1']),
    ])
    def test_should_filter_equals(self, lookup, value, expected_name_list):
        test_list = TestDatabase.populate_list_for_test()
        filtered = Database.filter_equals(lookup, value, test_list)
        assert len(filtered) == len(expected_name_list)
        assert [obj.name for obj in filtered] == expected_name_list

    @pytest.mark.parametrize("lookup,value,expected_name_list", [
        ('price', 50, ['Product 1', None, 'Item 2']),
        ('price', 35, ['Item 2']),
    ])
    def test_should_filter_lt(self, lookup, value, expected_name_list):
        test_list = TestDatabase.populate_list_for_test()
        filtered = Database.filter_lt(lookup, value, test_list)
        assert len(filtered) == len(expected_name_list)
        assert [obj.name for obj in filtered] == expected_name_list

    @pytest.mark.parametrize("lookup,value,expected_name_list", [
        ('name', 'Item', ['Item 1', 'Item 2']),
        ('name', 'Product', ['Product 1']),
    ])
    def test_should_filter_contains(self, lookup, value, expected_name_list):
        test_list = TestDatabase.populate_list_for_test()
        filtered = Database.filter_contains(lookup, value, test_list)
        assert len(filtered) == len(expected_name_list)
        assert [obj.name for obj in filtered] == expected_name_list
