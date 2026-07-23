from common_enum import VehicleType

class Vehicle:

    def __init__(self, vehicle_id: str, vehicle_type: VehicleType) -> None:
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type