#!/usr/bin/python3

from datetime import datetime
from sql_connection import get_sql_connection

# Function to insert an order into the database
def insert_order(connection, order):
    cursor = connection.cursor()

    # SQL query to insert order information into the "orders" table
    order_query = ("INSERT INTO orders "
                   "(customer_name, total, datetime)"
                   "VALUES (%s, %s, %s)")

    # Data for the order query, including customer name, total, and current datetime
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    # Execute the order query and retrieve the last inserted order ID
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # SQL query to insert order details into the "order_details" table
    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    # Data for the order details query
    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])

    # Execute the order details query with multiple rows of data
    cursor.executemany(order_details_query, order_details_data)

    # Commit the changes to the database
    connection.commit()

    # Return the inserted order ID
    return order_id

# Function to retrieve order details based on the order ID
def get_order_details(connection, order_id):
    cursor = connection.cursor()

    # SQL query to select order details and related product information
    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
            "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    # Data for the query, including the order ID
    data = (order_id, )

    # Execute the query
    cursor.execute(query, data)

    # Retrieve the records from the query result
    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    # Close the cursor
    cursor.close()

    # Return the order details records
    return records

# Function to retrieve all orders from the database
def get_all_orders(connection):
    cursor = connection.cursor()

    # SQL query to select all orders
    query = ("SELECT * FROM orders")

    # Execute the query
    cursor.execute(query)

    # Retrieve the orders from the query result
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    # Close the cursor
    cursor.close()

    # Append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    # Return the response containing all orders with their order details
    return response

if __name__ == '__main__':
    # Get the SQL connection
    connection = get_sql_connection()
    print(get_all_orders(connection))
