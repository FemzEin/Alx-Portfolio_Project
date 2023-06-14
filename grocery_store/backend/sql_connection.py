#!/usr/bin/python3

import mysql.connector

__cnx = None

# Function to establish a MySQL database connection
def get_sql_connection():
  print("Opening mysql connection")
  global __cnx

  # Check if a connection already exists, if not, establish a new connection
  if __cnx is None:
    __cnx = mysql.connector.connect(user='root', password='albert', host='127.0.0.1', database='grocery_store')

  # Return the connection object
  return __cnx
