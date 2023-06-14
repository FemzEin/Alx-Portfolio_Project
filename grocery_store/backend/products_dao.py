#!/usr/bin/python3

from sql_connection import get_sql_connection

# Function to retrieve all products from the database
def get_all_products(connection):
    cursor = connection.cursor()

    # SQL query to select all products with their unit of measure information
    query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
             "FROM products INNER JOIN uom ON products.uom_id=uom.uom_id")

    # Execute the query
    cursor.execute(query)

    # Retrieve the products from the query result
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })

    # Return the response containing all products with their details
    return response

# Function to insert a new product into the database
def insert_new_product(connection, product):
    cursor = connection.cursor()

    # SQL query to insert product information into the "products" table
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit)"
             "VALUES (%s, %s, %s)")

    # Data for the query, including product name, unit of measure ID, and price per unit
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    # Execute the query and commit the changes to the database
    cursor.execute(query, data)
    connection.commit()

    # Return the last inserted product ID
    return cursor.lastrowid

# Function to delete a product from the database
def delete_product(connection, product_id):
    cursor = connection.cursor()

    # SQL query to delete a product from the "products" table based on the product ID
    query = ("DELETE FROM products WHERE product_id=" + str(product_id))

    # Execute the query and commit the changes to the database
    cursor.execute(query)
    connection.commit()

    # Return the last deleted product ID
    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': '1',
        'price_per_unit': 10
    }))
