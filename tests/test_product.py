from src.product import Product
import unittest


class TestProduct(unittest.TestCase):
    def test_product_attributes(self):
        product = Product(
            product="Product",
            grocycode="12345",
            font_family="Arial",
            due_date="2020-01-01",
        )
        self.assertEqual(product.name, "Product")
        self.assertEqual(product.grocycode, "12345")
        self.assertEqual(product.font_family, "Arial")
        self.assertEqual(product.due_date, "2020-01-01")
