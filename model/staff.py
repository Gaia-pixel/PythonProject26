from dataclasses import dataclass

@dataclass
class Staff:
    staff_id : int
    first_name : str
    last_name : str
    email : str
    phone : str
    active : str
    store_id : int
    manager_id : int

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def __eq__(self, other):
        return self.staff_id == other.staff_id
    def __hash__(self):
        return hash(self.staff_id)