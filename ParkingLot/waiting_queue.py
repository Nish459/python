from vehicle import Vehicle
from common_enum import VehicleType

class WaitingQueue:
    def __init__(self) -> None:
        self.queue = []

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.queue.append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle) -> None:
        if self.queue and vehicle in self.queue:
            self.queue.remove(vehicle)
    
    def notify(self, vehicle_type: VehicleType) -> Vehicle:
        if self.queue:
            for vehicle in self.queue:
                if vehicle.vehicle_type == vehicle_type:
                    self.queue.remove(vehicle)
                    return vehicle
            return None

    def __str__(self) -> str:
        return f"Waiting Queue: {self.queue}"