from fastapi import APIRouter, HTTPException 
from db_handler.dtatabase import save_order_to_db
import uuid
from models.pizza import OrderRequest
router = APIRouter()

@router.get("/menu")
def get_menu():
    return [
        {"name": "Margherita", "price": 10.0},
        {"name": "Pepperoni", "price": 12.5},
        {"name": "Vegan", "price": 11.0}
    ]

@router.post("/orders")
def create_order(order: OrderRequest):

    # check if list is empty, is so raise an exception
    if len(OrderRequest.pizzas) == 0 :
        raise HTTPException(status=400, detail="list is empty")

    else:

        # calc the total price of the pizzas
        for pizza in OrderRequest.pizzas:
            total_price+=pizza.price

        # create a dictionary with the order details 
        cust_id=str(uuid.uuid4())  #generate a randome id 
        order={
            "customer_id" : cust_id, 
            "customer" : OrderRequest.customer_name,
            "pizzas_list" : OrderRequest.pizzas,
        }

        # save order to db
        saved = save_order_to_db(order)

        # check if the order was actually saved, if not raise an exception
        if not saved :
            raise HTTPException(status=400, detail="order failed")

        # if the order was saved, send confirmation
        return[

            {"Order saved!, total price:" : total_price},
            { "order ID:": cust_id},
        ]

