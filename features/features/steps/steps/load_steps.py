"""
Load steps for Behave BDD tests
"""

from behave import given
from service.models import Product


@given("the following products")
def step_impl(context):
    """Delete all Products and load new ones"""

    Product.remove_all()

    for row in context.table:
        product = Product()
        product.deserialize(row.as_dict())
        product.create()
