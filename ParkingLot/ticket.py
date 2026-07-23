from vehicle import Vehicle
from datetime import datetime
import uuid
from common_enum import PaymentStatus
from parking_spot import ParkingSpot

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot) -> None:
        self.ticket_id = uuid.uuid4()
        self.parking_spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None
        self.vehicle_id = vehicle.vehicle_id
        self.status = PaymentStatus.PENDING

    def __str__(self) -> str:
        return f"Ticket ID: {self.ticket_id}, Vehicle ID: {self.vehicle_id}, Parking Spot: {self.parking_spot}, Entry Time: {self.entry_time}, Exit Time: {self.exit_time}, Status: {self.status}"