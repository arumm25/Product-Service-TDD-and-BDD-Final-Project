"""
Product Service Routes
"""

import os
import logging
from flask import Flask, jsonify, request, abort
from service.models import Product, Category, DataValidationError


# Create Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URI",
    "sqlite:///products.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# HTTP status codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404


@app.route("/")
def index():
    """Root URL response"""
    return jsonify(
        name="Product REST API Service",
        version="1.0",
        status="running"
    ), HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on its id
    """

    app.logger.info("Request to retrieve Product with id: %s", product_id)

    product = Product.find(product_id)

    if not product:
        abort(
            HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found."
        )

    app.logger.info("Returning Product: %s", product.name)

    return jsonify(product.serialize()), HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product

    This endpoint will update a Product based on its id
    """

    app.logger.info("Request to update Product with id: %s", product_id)

    product = Product.find(product_id)

    if not product:
        abort(
            HTTP_404_NOT_FOUND,
            f"Product with id '{product_id}' was not found."
        )

    data = request.get_json()

    if not data:
        abort(HTTP_400_BAD_REQUEST, "No input data provided")

    try:
        product.deserialize(data)
        product.id = product_id
        product.update()
    except DataValidationError as error:
        abort(HTTP_400_BAD_REQUEST, str(error))

    app.logger.info("Product with ID [%s] updated.", product.id)

    return jsonify(product.serialize()), HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based on its id
    """

    app.logger.info("Request to delete Product with id: %s", product_id)

    product = Product.find(product_id)

    if product:
        product.delete()

    app.logger.info("Product with ID [%s] delete complete.", product_id)

    return "", HTTP_204_NO_CONTENT


@app.route("/products", methods=["GET"])
def list_products():
    """
    List all Products

    This endpoint will list Products and can filter by:
    name, category, or available status.
    """

    app.logger.info("Request to list Products...")

    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        app.logger.info("Find by name: %s", name)
        products = Product.find_by_name(name)

    elif category:
        app.logger.info("Find by category: %s", category)
        try:
            products = Product.find_by_category(Category[category.upper()])
        except KeyError:
            abort(
                HTTP_400_BAD_REQUEST,
                f"Invalid category value: {category}"
            )

    elif available:
        app.logger.info("Find by availability: %s", available)
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)

    else:
        app.logger.info("Find all Products")
        products = Product.all()

    results = [product.serialize() for product in products]

    app.logger.info("Returning %d products", len(results))

    return jsonify(results), HTTP_200_OK


@app.errorhandler(HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles 404 errors"""
    return jsonify(
        error="Not Found",
        message=str(error.description)
    ), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles 400 errors"""
    return jsonify(
        error="Bad Request",
        message=str(error.description)
    ), HTTP_400_BAD_REQUEST
