
from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    customer_name: Annotated[str, Field(min_length=2)]
    product_name: Annotated[str, Field(min_length=2)]
    quantity: Annotated[int, Field(gt=0)]

@dataclass
class Product:
    name: str
    price: float
    stock: int 

    def reduce_stock(self, quantity):
        if quantity <= 0 or quantity > self.stock:
            raise ValueError("Invalid quantity")
        self.stock -= quantity
        

    def restock(self, quantity):
        if quantity <= 0:
            raise ValueError("Invalid quantity")
        self.stock += quantity
        