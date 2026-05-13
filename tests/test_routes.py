"""
Test cases for Product Service Routes
"""

import os
import logging
from unittest import TestCase

from wsgi import app
from service.models import Product, Category, db
from service.common import status
from tests.factories import ProductFactory


BASE_URL = "/products"

DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/testdb"
)


class TestProductRoutes(TestCase):
    """Product Routes Test Cases"""

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
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    def test_read_product(self):
        """It should Read a single Product"""
        product = ProductFactory()
        product.create()

        response = self.client.get(f"{BASE_URL}/{product.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["available"], product.available)
        self.assertEqual(data["category"], product.category.name)

    def test_update_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.create()

        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        data["description"] = "This is an updated description"

        response = self.client.put(
            f"{BASE_URL}/{product.id}",
            json=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "This is an updated description")
        self.assertEqual(updated_product["id"], product.id)

    def test_delete_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()

        response = self.client.delete(f"{BASE_URL}/{product.id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        products = ProductFactory.create_batch(5)

        for product in products:
            product.create()

        response = self.client.get(BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_products_by_name(self):
        """It should List Products by Name"""
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        test_name = products[0].name

        response = self.client.get(
            BASE_URL,
            query_string={"name": test_name}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_list_products_by_category(self):
        """It should List Products by Category"""
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        test_category = products[0].category

        response = self.client.get(
            BASE_URL,
            query_string={"category": test_category.name}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        for product in data:
            self.assertEqual(product["category"], test_category.name)

    def test_list_products_by_availability(self):
        """It should List Products by Availability"""
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        test_available = products[0].available

        response = self.client.get(
            BASE_URL,
            query_string={"available": str(test_available).lower()}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        for product in data:
            self.assertEqual(product["available"], test_available)
