from vehicle import Vehicle
from ticket import Ticket
from gate import Gate
from parking_spot import ParkingSpot

class EntryGate(Gate):
    def generate_ticket(self, vehicle: Vehicle, spot: ParkingSpot) -> Ticket:
        return Ticket(vehicle, spot)