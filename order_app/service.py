import logging

from .database import OrderDatabase
from .models import OrderRequest
from .registry import ProductRegistry

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, registry: ProductRegistry, database: OrderDatabase):
        self.registry = registry
        self.database = database
        

    def process_order(self, request: OrderRequest):
        product = self.registry.get_product(request.product_name)
        if product == "Product not found":
            logger.warning("Product not found")
            return "Product not found"
        if product.stock < request.quantity:
            logger.warning(f"Not enough stock left to process the order: {request.product_name} by {request.customer_name}")
            return f"Not enough stock left to process the order: {request.product_name} by {request.customer_name}"
        product.reduce_stock(request.quantity)
        total = product.price * request.quantity
        customer_id = self.database.save_customer(request.customer_name)
        self.database.save_order(customer_id=customer_id, 
                                 product_name= request.product_name,
                                 quantity= request.quantity,
                                 unit_price= product.price,
                                 total= total)
        logger.info("Order processed: customer=%s product=%s quantity=%s total=%s",
                    request.customer_name,
                    request.product_name,
                    request.quantity,
                    total)
        return total
