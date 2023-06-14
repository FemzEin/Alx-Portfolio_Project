#!/usr/bin/python3

# Function to retrieve all unit of measure (UOM) records from the database
def get_uoms(connection):
    cursor = connection.cursor()

    # SQL query to select all UOM records from the "uom" table
    query = ("SELECT * FROM uom")

    # Execute the query
    cursor.execute(query)

    # Retrieve the UOM records from the query result
    response = []
    for (uom_id, uom_name) in cursor:
        response.append({
            'uom_id': uom_id,
            'uom_name': uom_name
        })

    # Return the response containing all UOM records
    return response


if __name__ == '__main__':
    from sql_connection import get_sql_connection

    # Establish a SQL connection
    connection = get_sql_connection()

    # Uncomment the line below to print all UOM records
    # print(get_all_products(connection))

    # Print the UOM records obtained from the database
    print(get_uoms(connection))
