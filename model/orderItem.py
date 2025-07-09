from dataclasses import dataclass

@dataclass
class OrderItem:
    order_id : int
    item_id : int
    product_id : int
    quantity : int
    list_price : float
    discount : float

    def __str__(self):
        return f"{self.order_id} {self.item_id}"
    def __eq__(self, other):
        return (self.order_id, self.item_id) == (other.order_id, other.item_id)
    def __hash__(self):
        return hash((self.order_id, self.item_id))