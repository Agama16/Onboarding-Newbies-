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

    if len(OrderRequest.pizzas) == 0 :
        raise HTTPException(status=400, detail="list is empty")
    else:
        for pizza in OrderRequest.pizzas:
            total_price+=pizza.price
 
        cust_id=str(uuid.uuid4())  
        order={
            "customer_id" : cust_id, 
            "customer" : OrderRequest.customer_name,
            "pizzas_list" : OrderRequest.pizzas,
        }
        saved = save_order_to_db(order)

        if not saved :
            raise HTTPException(status=400, detail="order failed")
      
        return[

            {"Order saved!, total price:" : total_price},
            { "order ID:": cust_id},
        ]

