import enum

class HospitalStatus(str, enum.Enum):
    open = "open"
    busy = "busy"
    closed = "closed"
