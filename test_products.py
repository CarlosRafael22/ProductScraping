from products import Product, ProductDatabase


def create_test_product():
    props = {
        'name': 'Cadeira Gamer DAZZ Prime-X Preta/Azul',
        'price_str': 'R$ 999,99',
        'price': 999.99,
        'link': '/produto/1292680481?pfm_carac=cadeira%20gamer&pfm_index=19&pfm_page=search&pfm_pos=grid&pfm_type=search_page',
        'image_url': None
    }
    product = Product(props)
    return product


class TestProduct:
    def test_should_create_product(self):
        props = {
            'name': 'Cadeira Gamer DAZZ Prime-X Preta/Azul',
            'price_str': 'R$ 999,99',
            'price': 999.99,
            'link': '/produto/1292680481?pfm_carac=cadeira%20gamer&pfm_index=19&pfm_page=search&pfm_pos=grid&pfm_type=search_page',
            'image_url': None
        }
        product = Product(props)
        assert product.name == props['name']
        assert product.price_str == props['price_str']
        assert product.price == props['price']
        assert product.link == props['link']
        assert product.image_url == props['image_url']
        assert product.store == None


class TestProductDatabase:
    def test_should_add_product(self):
        ProductDatabase.clear_database()
        product = create_test_product()
        # import pdb; pdb.set_trace()
        previous_total = ProductDatabase.get_products_total()

        ProductDatabase.add_product(product)
        total = ProductDatabase.get_products_total()
        assert total == previous_total + 1
    
    # def test_should_filter_from_inheritance(self):
    #     product = create_test_product()
    #     props = {
    #         'name': 'Cadeira Escritorio Luxx',
    #         'price_str': 'R$ 299,99',
    #         'price': 299.99,
    #         'link': '/produto/1292680481?pfm_carac=cadeira%20gamer&pfm_index=19&pfm_page=search&pfm_pos=grid&pfm_type=search_page',
    #         'image_url': None
    #     }
    #     product = Product(props)
    #     previous_total = ProductDatabase.get_products_total()
    #     # import pdb; pdb.set_trace()
    #     filtered = ProductDatabase.filter(ProductDatabase.products, price__lt=400)
    #     assert len(filtered) == 1

    def test_should_filter(self):
        ProductDatabase.clear_database()
        product = create_test_product()
        props = {
            'name': 'Cadeira Escritorio Luxx Premium',
            'price_str': 'R$ 599,99',
            'price': 599.99,
            'link': '/produto/1292680481?pfm_carac=cadeira%20gamer&pfm_index=19&pfm_page=search&pfm_pos=grid&pfm_type=search_page',
            'image_url': None
        }
        product = Product(props)
        # previous_total = ProductDatabase.get_products_total()
        # import pdb; pdb.set_trace()
        filtered = ProductDatabase.filter(price__lt=800, price__gte=400)
        assert len(filtered) == 1
        assert filtered[0].name == product.name
    
    def test_should_clear_database(self):
        previous_total = ProductDatabase.get_products_total()
        assert previous_total != 0

        ProductDatabase.clear_database()
        assert ProductDatabase.get_products_total() == 0
        assert ProductDatabase.products == []


