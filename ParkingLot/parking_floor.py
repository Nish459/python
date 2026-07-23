from parking_spot import ParkingSpot
from typing import List

class ParkingFloor:
    def __init__(self, floor_id: str) -> None:
        self.floor_id = floor_id
        self.spots: List[ParkingSpot] = []

    def add_spot(self, spot: ParkingSpot) -> None:
        self.spots.append(spot)

    def get_spot(self, spot_id: str) -> ParkingSpot:
        for spot in self.spots:
            if spot.spot_id == spot_id:
                return spot
        return None