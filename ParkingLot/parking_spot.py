import uuid
from common_enum import VehicleType
from vehicle import Vehicle

class ParkingSpot:
    def __init__(self, vehicle_type: VehicleType) -> None:
        self.vehicle_type = vehicle_type
        self.is_available = True
        self.vehicle_id = None
        self.spot_id = uuid.uuid4()

    def can_park_vehicle(self, vehicle: Vehicle) -> bool:
        return self.is_available and self.vehicle_type == vehicle.vehicle_type

    def vacate_spot(self) -> None:
        self.is_available = True
        self.vehicle_id = None

    def park_vehicle(self, vehicle: Vehicle) -> None:
        self.is_available = False
        self.vehicle_id = vehicle.vehicle_id

    def __str__(self) -> str:
        return f"Spot ID: {self.spot_id}, Type: {self.vehicle_type}, Available: {self.is_available}"
