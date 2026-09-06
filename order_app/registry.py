from dataclasses import dataclass

from .models import Product


class ProductRegistry:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        if product.name in self.products:
            return "Product already exists"
        self.products[product.name] = product
        return "Product added succesfully"

    def get_product(self, name):
        if name not in self.products:
            return "Product not found"
        return self.products[name]