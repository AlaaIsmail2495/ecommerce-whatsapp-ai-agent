import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("ECOMMERCE_API_URL","http://127.0.0.1:8000")


def list_categories() ->dict :
    """Retrieve all available product categories in the store. """
    try:
        response = requests.get(f"{BASE_URL}/categories", timeout=5)
        if response.status_code == 200 :
            return {"success": True, "categories": response.json()}
        return {"success": False, "error": f"Failed with status {response.status_code}"}        

    except Exception as e:
        return {"success": False, "error": str(e)}


def search_products(keyword: str = "", category_id: int = None, in_stock_only: bool = False) ->dict :
    """Search products in the catalog by keyword, category, or stock status. 

    Args:
        keyword: Search text to match product name.
        category_id: Optional category ID to filter by.
        in_stock_only: Set to True to filter out products with zero stock. 
    be smart and search with sub text like "prod" instead of products.           
    """
    params = {}
    if keyword:
        params["search"] = keyword
    if category_id is not None :
        params["category_id"] = category_id
    if in_stock_only :
        params["in_stock_only"] = True

    try :
        response = requests.get(f"{BASE_URL}/products", params=params , timeout=5)
        if response.status_code == 200 :
            products = response.json()
            return {"success": True, "count": len(products), "products": products}
        return {"success": False, "error": f"Failed with status {response.status_code}"}    

    except Exception as e :
        return {"success": False, "error": str(e)}


def get_product_details(product_id: int) -> dict:
    """Get full details, price, and current stock for a specific product by its ID.
    Args:
        product_id: The integer ID of the product.
    """
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}",timeout=5)
        if response.status_code == 200 :
            return {"success": True, "product": response.json()}
        return {"success": False, "error": f"Product with ID {product_id} not found."}    

    except Exception as e :
        return {"success": False, "error": str(e)}


def get_customer_cart(customer_name: str) ->dict :
    """Get the current shopping cart and view the items in and subtotal for a customer.

    Args:
        customer_name: The customer username or phone number.
    """
    try: 
        response = requests.get(f"{BASE_URL}/cart/{customer_name}", timeout=5)
        if response.status_code == 200 : 
            return {"success": True, "cart": response.json()}
        return {"success": False, "error": f"Couldn't retrieve cart for {customer_name}"}    

    except Exception as e :
        return {"success": False, "error": str(e)}


def add_item_to_cart(customer_name: str, product_id: int, quantity: int =1 ) ->dict :
    """Add product to the customer's shopping cart.
    Args:
        customer_name: The customer username or phone number.
        product_id: The integer ID of product to add.
        quantity: The number of units to add (defaults to 1).
    """
    payload = {
        "customer_name": customer_name,
        "product_id": product_id,
        "quantity": quantity
    }
    try: 
        response = requests.post(f"{BASE_URL}/cart/items", json=payload, timeout=5)
        if response.status_code == 201 :
            return {"success": True, "added_item": response.json()}
        return {"success": False, "error": response.json().get("detail", "Failed to add to cart.")}    

    except Exception as e :
        return {"success": False, "error": str(e)}


def remove_cart_item(item_id: int) ->dict :
    """Remove a specific item from a shopping cart by its item ID.
    Args:
        item_id: The integer ID of the cart item to remove.
    """
    try: 
        response = requests.delete(f"{BASE_URL}/cart/items/{item_id}", timeout=5)
        if response.status_code == 200 :
            return {"success": True, "message":f"Cart item {item_id} removed."}
        return {"success": False, "error": f"Item {item_id} not found in cart."}    

    except Exception as e :
        return {"success": False, "error": str(e)}


def clear_customer_cart(customer_name: str) ->dict :
    """Clear all items from a customer's cart.
    Args:
        customer_name: The customer username or phone number.
    """
    try: 
        response = requests.delete(f"{BASE_URL}/cart/{customer_name}", timeout=5)
        if response.status_code == 404 :
            response = requests.delete(f"{BASE_URL}/cart/clear/{customer_name}", timeout=5)

        if response.status_code == 200 :
            return {"success": True, "message": "Cart cleared successfully."} 

        return {"success": False, "error": "Failed to clear cart"}       

    except Exception as e :
        return {"success": False, "error": str(e)}


def checkout_cart(customer_name: str, shipping_address: str ="") ->dict:
    """Place an order from items in the customer's cart and deduct stock and clear the cart.
    Args:
        customer_name: The customer username or phone number.
        shipping_address: The delivery address for the order.
    """
    payload = {
        "customer_name": customer_name,
        "customer_phone": customer_name
    }
    try: 
        response = requests.post(f"{BASE_URL}/orders/checkout", json=payload, timeout=5)
        if response.status_code == 404 :
            response = requests.post(f"{BASE_URL}/checkout", json=payload, timeout=5) 
        if response.status_code == 201 :
            order_info = response.json()
            if shipping_address :
                order_info["shipping_address"] = shipping_address
            return {"success": True, "order": order_info} 

        error_detail = response.json().get("detail", "checkout failed.") if response.content else f"Status {response.status_code}"
        return {"success": False, "error": error_detail}

    except Exception as e :
        return {"success": False, "error": str(e)}



def track_order(order_id: int) ->dict :
    """Retrieve details and shipping status for an existing order by ID.
    Args: 
        order_id: The numeric ID of an existing order to track.
    """
    try: 
        response = requests.get(f"{BASE_URL}/orders/{order_id}", timeout=5)
        if response.status_code == 200 :
            return {"success": True, "order": response.json()}

        detail = response.json().get("detail", "Order not found") if response.content else f"Status {response.status_code}"
        return {"success": False, "error": detail}       

    except Exception as e :
        return {"success": False, "error": str(e)}


def cancel_order(order_id: int) ->dict:
    """Cancel an active order and restore inventory stock.
    Args:
        order_id: The numeric ID of the order to cancel.
    """
    try:
        response = requests.put(f"{BASE_URL}/orders/{order_id}/cancel", timeout=5)
        if response.status_code == 200 :
            return {"success": True, "order": response.json()}

        detail = response.json().get("detail", "Cannot cancel order") if response.content else f"Status {response.status_code}"
        return {"success": False, "error": detail}       

    except Exception as e :
        return {"success": False, "error": str(e)}

ALL_STORE_TOOLS = [
    list_categories,
    search_products,
    get_product_details,
    get_customer_cart,
    add_item_to_cart,
    remove_cart_item,
    clear_customer_cart,
    checkout_cart,
    track_order,
    cancel_order
]
