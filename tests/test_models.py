"""
Test cases for Product Model
"""

import os
import logging
from unittest import TestCase

from wsgi import app
from service.models import Product, Category, db
from tests.factories import ProductFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/testdb"
)


class TestProductModel(TestCase):
    """Product Model Test Cases"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        pass

    def setUp(self):
        """Runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.create()

        self.assertIsNotNone(product.id)

        found_product = Product.find(product.id)

        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.create()

        self.assertIsNotNone(product.id)

        product.description = "This is an updated description"
        original_id = product.id
        product.update()

        self.assertEqual(product.id, original_id)

        found_product = Product.find(product.id)
        self.assertEqual(found_product.description, "This is an updated description")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()

        self.assertIsNotNone(product.id)

        product.delete()

        found_product = Product.find(product.id)
        self.assertIsNone(found_product)

    def test_list_all_products(self):
        """It should List all Products"""
        products = Product.all()
        self.assertEqual(products, [])

        for product in ProductFactory.create_batch(5):
            product.create()

        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)

        for product in products:
            product.create()

        name = products[0].name
        found_products = Product.find_by_name(name)

        self.assertGreaterEqual(found_products.count(), 1)
        self.assertEqual(found_products[0].name, name)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        category = products[0].category
        count = len([product for product in products if product.category == category])

        found_products = Product.find_by_category(category)

        self.assertEqual(found_products.count(), count)

        for product in found_products:
            self.assertEqual(product.category, category)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        available = products[0].available
        count = len([product for product in products if product.available == available])

        found_products = Product.find_by_availability(available)

        self.assertEqual(found_products.count(), count)

        for product in found_products:
            self.assertEqual(product.available, available)
