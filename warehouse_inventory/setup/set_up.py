from dotenv import load_dotenv
import os
import mysql.connector

# Initialize data after database implementation
# Only do this if the inventory_db is implemented already
# and the necessary tables are created.

# Instead first get the django working,
# make sure makemigrations and migrate are run first
# this will initialize the database, and all the tables

# Initialise env
load_dotenv()

# Initialise database connections
db_connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASS")
)

db_cursor = db_connection.cursor()

categories = {}
# Read CSV
# Connect to database
# Uploads data to database
# And Uploads images to contents folder in Django
