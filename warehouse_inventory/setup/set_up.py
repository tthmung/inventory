from dotenv import load_dotenv
import os
import mysql.connector
import csv
import urllib.request
from urllib.parse import urlparse
from os.path import splitext

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

# Select database
db_cursor.execute("USE inventory_db")

# Reset Tables in case there is anything in there
db_cursor.execute("DELETE FROM inventory_item_category")
db_cursor.execute("DELETE FROM inventory_item")

# Initial categories we will work with
categories = ["Chemical", "Metal", "Organic Product",
              "Electronic", "Textile And Apparel", "Medical"]

# SQL query for inserting categories
db_categories = "INSERT INTO inventory_item_category (name) VALUES (%s)"

# Loop through categories and insert each one
for category in categories:
    db_cursor.execute(db_categories, (category,))  # Note the comma to create a tuple with a single element
    db_connection.commit()

# Read CSV
# Connect to database
# Uploads data to database
# And Uploads images to contents folder in Django

target_dir = "../uploads"

file = open("inv_data.csv", "r")
csv_read = csv.reader(file)

# Skip first row
next(csv_read)
for row in csv_read:

    # Get the filename from URL
    url_path = urlparse(row[5]).path
    img_filename = os.path.basename(url_path)

    # Get the file extension
    _, img_extension = splitext(img_filename)

    # Build the image path
    img_name = f"{row[0]}{img_extension}"
    img_path = os.path.join(target_dir, img_name)

    try:
        urllib.request.urlretrieve(row[5], img_path)

        # Upload data to database
        db_sql = "INSERT INTO inventory_item (id, name, descriptions, quantity, category_id, image) VALUES (%s, %s, %s, %s, %s, %s)"

        # Remove the url from the row and append the new image name
        row[5] = img_name

        # Get the id of the category
        db_cursor.execute("SELECT id FROM inventory_item_category WHERE name = %s", (row[4], ))
        result = db_cursor.fetchone()
        row[4] = result[0]

        # Commit sql
        db_cursor.execute(db_sql, row)
        db_connection.commit()

    except urllib.error.HTTPError as e:
        print(f"Error downloading image {row[5]}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Close the cursor and connection
db_cursor.close()
db_connection.close()
