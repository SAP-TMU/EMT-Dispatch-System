from enum import Enum

class AmbulanceStatus(str, Enum):
    available = "available"
    en_route_to_patient = "en_route_to_patient"
    at_scene = "at_scene"
    en_route_to_hospital = "en_route_to_hospital"
    at_hospital = "at_hospital"
    busy = "busy"  # can mean waiting for return-to-base or cleanup
