from pydantic import BaseModel, Field
from typing import List

class PizzaItem(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=1)
    pizzas: List[PizzaItem]
