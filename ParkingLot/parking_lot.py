from parking_floor import ParkingFloor
from entry_gate import EntryGate
from exit_gate import ExitGate
from typing import List
from vehicle import Vehicle
from parking_spot import ParkingSpot
from ticket import Ticket
from common_enum import PaymentMethod
from fee_calculator import FeeCalculator
from threading import Lock
from waiting_queue import WaitingQueue

class ParkingLot:
    def __init__(self, name: str) -> None:
        self.name = name
        self.floors: List[ParkingFloor] = []
        self.entry_gates: List[EntryGate] = []
        self.exit_gates: List[ExitGate] = []
        self.lock = Lock()
        self.waiting_queue = WaitingQueue()
        self.active_tickets = {}

    def _get_available_spot(self, vehicle: Vehicle) -> ParkingSpot:
        for floor in self.floors:
            for spot in floor.spots:
                if spot.can_park_vehicle(vehicle):
                    return spot
        return None

    def assign_spot(self, entry_gate: EntryGate, vehicle: Vehicle) -> Ticket | None:
        with self.lock:
            spot = self._get_available_spot(vehicle)
            if spot:
                spot.park_vehicle(vehicle)
                ticket = entry_gate.generate_ticket(vehicle, spot)
                self.active_tickets[vehicle.vehicle_id] = ticket
                return ticket
            else:
                self.waiting_queue.add_vehicle(vehicle)
                return None

    def process_exit(self, entry_gate: EntryGate, exit_gate: ExitGate, ticket: Ticket, payment_method: PaymentMethod, fee_calculator: FeeCalculator) -> None:
        try:
            exit_gate.exit(ticket, payment_method, fee_calculator)
            self.free_spot(entry_gate, ticket.parking_spot)
        except Exception as e:
            raise Exception("Failed to process exit")
            
    def free_spot(self, entry_gate: EntryGate, spot: ParkingSpot) -> None:
        del self.active_tickets[spot.vehicle_id]
        spot.vacate_spot()
        vehicle = self.waiting_queue.notify(spot.vehicle_type)
        if vehicle:
            spot.park_vehicle(vehicle)
            ticket = entry_gate.generate_ticket(vehicle, spot)
            self.active_tickets[vehicle.vehicle_id] = ticket
        return