import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(0)
        return extracted_string

    return ""

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


def calculate_order_price(menu, order):
    order_id = 45
    print("order_id\item_id\tquantity\ttotal_Price")
    for food_name, quantity in order.items():
        item_index = menu["food_name"].index(food_name)

        item_id = menu["item_id"][item_index]
        price = menu["price"][item_index]
        total_price = price * quantity