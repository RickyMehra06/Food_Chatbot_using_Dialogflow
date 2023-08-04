from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import utils

app = FastAPI()

inprogress_orders = {}

menu = {"item_id": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        "food_name": ["Dal Makhani", "Butter Paneer", "Pindi Chole", "Roti", "Naan", "Lachha Parantha", "Raita", "Rice", 
                      "Biryani", "Chole Bhature", "Paneer Tikka", "Malai Chaap", "Lassi", "Samosa", "Pizza"],
        "price" : [200, 300, 200, 25, 50, 50, 50, 100, 200, 100, 300, 250, 50, 20, 150]       
    }

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = utils.extract_session_id(output_contexts[0]["name"])

    print(f"Intent: {intent}") 
    print(f"parameters: {parameters}")  
    print(f"session_id: {session_id}") 

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    
    # Inserting individual items along with quantity in orders table
    for item_name, quantity in order.items():
        # finding the index of food_name
        item_index = menu["food_name"].index(item_name)

        item_id = menu["item_id"][item_index]
        price = menu["price"][item_index]
        total_price = price * quantity 

        rcode = db_helper.insert_order_items(next_order_id, item_id, item_name, quantity, total_price)

        if rcode == -1:
            return -1
    
     # Now inserting order tracking status
    db_helper.insert_order_tracking(next_order_id, "In-Process")

    return next_order_id


def complete_order(parameters: dict, session_id: str):

    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Your order has been placed with order id # {order_id}. " \
                           f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-items"]
    quantities = parameters.get("number", [1] * len(food_items))  # Use default value [1] if 'number' is missing

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
        else:
            current_food_dict = {}

        for food_item, quantity in zip(food_items, quantities):
            quantity = int(quantity)  # Convert the quantity to an integer
            if food_item in current_food_dict:
                current_food_dict[food_item] += quantity
            else:
                current_food_dict[food_item] = quantity

        inprogress_orders[session_id] = current_food_dict

        order_str = utils.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "remove_from_order ---- I'm having trouble finding your order. Sorry! Can you place a new order, please?"
        })

    food_items = parameters["food-items"]
    quantities = parameters.get("number", [1] * len(food_items))  # Use default value [1] if 'number' is missing
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []
    fulfillment_text = ""  # Initialize fulfillment_text with an empty string

    for item, quantity_to_remove in zip(food_items, quantities):
        if item not in current_order:
            no_such_items.append(item)
        else:
            quantity_to_remove = int(quantity_to_remove)
            quantity_in_order = current_order[item]

            if quantity_to_remove >= quantity_in_order:
                del current_order[item]
                removed_items.append(item)
            else:
                current_order[item] = quantity_in_order - quantity_to_remove
                removed_items.append(item)

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {", ".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f'Your current order does not have {", ".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = utils.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    
    if order_status:
        fulfillment_text = f"Your order status is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

 