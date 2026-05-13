"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    available = factory.Faker("boolean")
    category = factory.Iterator(
        [
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
