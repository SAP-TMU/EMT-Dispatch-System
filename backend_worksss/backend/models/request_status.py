import enum

class RequestStatus(str, enum.Enum):
    pending = "pending"
    assigned = "assigned"
    picked_up = "picked_up"
    completed = "completed"
    cancelled = "cancelled"
