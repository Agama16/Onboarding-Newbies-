from fastapi import APIRouter, HTTPException 
from db_handler.dtatabase import save_order_to_db
from uuid import uuid4
from typing import List, Dict, Any
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
def create_order(order: OrderRequest) -> List[Dict[str, Any]]:

    total_price=0
    
    if len(order.pizzas) == 0 :
        raise HTTPException(status=400, detail="list is empty")
    else:
        for pizza in order.pizzas:
            total_price+=pizza.price
 
        customer_id: str =str(uuid4())  # uuid is a python unique id generator 
        order_to_save: Dict[str, Any] ={
            "customer_id" : customer_id, 
            "customer" : order.customer_name,
            "pizzas_list" : order.pizzas,
        }
        saved: bool = save_order_to_db(order_to_save)
        
        if not saved :
            raise HTTPException(
                status_code=400, 
                detail="could not save the order, check that the order's details are valid and try again")
      
        return[
            {"Order saved!, total price:" : total_price},
            { "Order ID:": customer_id},
        ]

