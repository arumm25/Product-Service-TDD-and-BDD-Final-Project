Feature: The product service back-end
    As a Product Manager
    I need a RESTful catalog service
    So that I can keep track of all my products


Background:
    Given the following products
        | name    | description      | price | available | category   |
        | Hat     | A red fedora     | 59.95 | True      | CLOTHS     |
        | Shoes   | Blue shoes       | 89.99 | True      | CLOTHS     |
        | Hammer  | Heavy hammer     | 34.95 | False     | TOOLS      |
        | Car Wax | Car cleaning wax | 19.99 | False     | AUTOMOTIVE |


Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Product ID" field
    And I press the "Clear" button
    And I paste the "Product ID" field
    And I press the "Retrieve" button
    Then I should see "Hat" in the "Name" field


Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Product ID" field
    And I press the "Clear" button
    And I paste the "Product ID" field
    And I press the "Retrieve" button
    And I set the "Description" to "A green fedora"
    And I press the "Update" button
    Then I should see the message "Success"


Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Product ID" field
    And I press the "Clear" button
    And I paste the "Product ID" field
    And I press the "Retrieve" button
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"


Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Hammer" in the results
    And I should see "Car Wax" in the results


Scenario: Search Products by Category
    When I visit the "Home Page"
    And I set the "Category" to "CLOTHS"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Hammer" in the results
    And I should not see "Car Wax" in the results


Scenario: Search Products by Availability
    When I visit the "Home Page"
    And I set the "Available" to "True"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Hammer" in the results
    And I should not see "Car Wax" in the results


Scenario: Search Products by Name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Hammer" in the results
    And I should not see "Car Wax" in the results
