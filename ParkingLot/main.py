from fee_calculator import HourlyFeeCalculator
from parking_lot import ParkingLot
from parking_floor import ParkingFloor
from entry_gate import EntryGate
from exit_gate import ExitGate
from parking_spot import ParkingSpot

from vehicle import Vehicle
from common_enum import VehicleType, PaymentMethod

def main():
    try:
        parking_lot = ParkingLot("Main Parking Lot")

        parking_floor = ParkingFloor("1")
        parking_floor.add_spot(ParkingSpot(VehicleType.CAR))
        parking_floor.add_spot(ParkingSpot(VehicleType.BIKE))
        parking_floor.add_spot(ParkingSpot(VehicleType.TRUCK))
        parking_floor.add_spot(ParkingSpot(VehicleType.BUS))

        exit_gate = ExitGate(1)
        entry_gate = EntryGate(1)
        
        parking_lot.floors.append(parking_floor)
        
        parking_lot.entry_gates.append(entry_gate)
        parking_lot.exit_gates.append(exit_gate)

        vehicle_car_1 = Vehicle("1234567890", VehicleType.CAR)
        ticket_car_1 = parking_lot.assign_spot(entry_gate, vehicle_car_1)
        print(str(ticket_car_1))

        vehicle_bike_1 = Vehicle("1234567890", VehicleType.BIKE)
        ticket_bike_1 = parking_lot.assign_spot(entry_gate, vehicle_bike_1)
        print(str(ticket_bike_1))

        vehicle_car_2 = Vehicle("1234567890", VehicleType.CAR)
        ticket_car_2 = parking_lot.assign_spot(entry_gate, vehicle_car_2)
        print(str(ticket_car_2))

        # vehicle = Vehicle("1234567890", VehicleType.CAR)
        # ticket = parking_lot.assign_spot(entry_gate, vehicle)

        # vehicle = Vehicle("1234567890", VehicleType.CAR)
        # ticket = parking_lot.assign_spot(entry_gate, vehicle)
        
        
        fee_calculator = HourlyFeeCalculator()
        parking_lot.process_exit(entry_gate, exit_gate, ticket_car_1, PaymentMethod.CREDIT_CARD, fee_calculator)
        parking_lot.process_exit(entry_gate, exit_gate, ticket_bike_1, PaymentMethod.UPI, fee_calculator)
        parking_lot.process_exit(entry_gate, exit_gate, ticket_car_2, PaymentMethod.DEBIT_CARD, fee_calculator)
        
        print("Vehicle exited successfully")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()