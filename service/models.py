"""
Product Model
"""

import logging
from enum import Enum
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Category(Enum):
    """Enumeration of valid Product Categories"""

    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Class that represents a Product"""

    app = None

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.UNKNOWN)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product in the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product in the database"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Product from the database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = Decimal(str(data["price"]))

            available = data["available"]
            if isinstance(available, bool):
                self.available = available
            else:
                self.available = str(available).lower() in ["true", "1", "yes"]

            category = data["category"]
            if isinstance(category, Category):
                self.category = category
            else:
                self.category = Category[str(category).upper()]

        except KeyError as error:
            raise DataValidationError(
                f"Invalid product: missing {error.args[0]}"
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            ) from error
        except ValueError as error:
            raise DataValidationError(f"Invalid product: {error}") from error

        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Returns all Products"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        logger.info("Processing name query for %s", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """Returns all Products with the given category"""
        logger.info("Processing category query for %s", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by their availability"""
        logger.info("Processing availability query for %s", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def remove_all(cls):
        """Removes all Products from the database"""
        cls.query.delete()
        db.session.commit()
