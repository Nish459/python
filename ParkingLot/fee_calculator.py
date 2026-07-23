from abc import ABC, abstractmethod

class FeeCalculator(ABC):
    @abstractmethod
    def calculate_fee(self, duration: int) -> float:
        pass

class HourlyFeeCalculator(FeeCalculator):
    def calculate_fee(self, duration: float) -> float:
        return duration * 10

class DailyFeeCalculator(FeeCalculator):
    def calculate_fee(self, duration: int) -> float:
        return duration * 100

class WeeklyFeeCalculator(FeeCalculator):
    def calculate_fee(self, duration: int) -> float:
        return duration * 1000