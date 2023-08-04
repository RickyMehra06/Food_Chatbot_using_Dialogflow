import mysql.connector as connector

connection = connector.connect(host="localhost", user="root",password="12345", database="food_database")

# Function to get the next available order_id
def get_next_order_id():
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1
    

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = connection.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    values = (order_id, status)
    cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()

    print("Tracking has been inserted successfully!")
    

def insert_order_items(order_id, item_id, item_name, quantity, total_price):
    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO orders (order_id, item_id, item_name, quantity, total_price) VALUES (%s, %s, %s, %s, %s)"
        values = (order_id, item_id, item_name, quantity, total_price)

        cursor.execute(insert_query, values)

        connection.commit()
        cursor.close()

        print("Order items inserted successfully!")

        return 1

    except Exception as e:
        print(f"An error occurred while inserting order: {e}")
        # Rollback changes if necessary
        connection.rollback()

        return -1


def get_total_order_price(order_id):
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT SUM(total_price) FROM orders WHERE order_id = {order_id}"

    cursor.execute(query)
    result = cursor.fetchone()[0]
    
    cursor.close()

    return result


# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    cursor = connection.cursor()

    query = f"SELECT status FROM order_tracking WHERE order_id = {int(order_id)}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()

    if result:
        return result[0]
    else:
        return None


if __name__ == "__main__":
    print(get_next_order_id())

