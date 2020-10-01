# from database import Database

class Product:

    def __init__(self, product_attribute):
        self.name = product_attribute.get('name', None)
        self.price_str = product_attribute.get('price_str', None)
        self.price = product_attribute.get('price', None)
        self.link = product_attribute.get('link', None)
        self.image_url = product_attribute.get('image_url', None)
        self.store = product_attribute.get('store', None)

        ProductDatabase.add_product(self)
    
    def __str__(self):
        return f'{self.name} - {self.price_str}'
    
    def __repr__(self):
        return f'{self.name} - {self.price_str}'


class ProductDatabase():
    products = []

    @classmethod
    def get_products_total(cls):
        return len(cls.products)
    
    @property
    def total(self):
        return len(self.products)

    @classmethod
    def add_product(cls, product: Product):
        cls.products.append(product)