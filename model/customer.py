from dataclasses import dataclass

@dataclass
class Customer:
    customer_id : int
    first_name : str
    last_name : str
    phone : str
    email : str
    street : str
    city : str
    state : str
    zip_code : int

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def __eq__(self, other):
        return self.customer_id == other.customer_id
    def __hash__(self):
        return hash(self.customer_id)