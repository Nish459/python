"""
Open Close Principle (OCP)

A class should be open for extension and close for modification.
It should be easy to add features without changing the existing logic, and it helps to test the new changes
effectively.

How to Structure this in an Interview
1. State the principle clearly:

"OCP says a class should be open for extension but closed for modification."

2. Explain the problem (the "bad" way):

"If we use if/elif chains to handle different discount types, every time we add a new type — 
like a seasonal discount — we have to modify the existing calculate_discount method. 
This risks breaking already-working logic and requires re-testing everything."

3. Explain the solution (the "good" way):

"Instead, we define an abstract DiscountStrategy with a calculate_discount method. 
Each discount type is its own class — FlatDiscount, PercentageDiscount, etc. 
The DiscountCalculator just calls discount.calculate_discount(amount) without knowing which type it is."

4. Drive the point home:

"So when the business says 'add a buy-one-get-one-free discount,'
I create a new BuyOneGetOneFreeStrategy class. I don't touch DiscountCalculator, FlatDiscount, 
or PercentageDiscount at all.
Zero risk to existing functionality."

5. Mention the real-world benefit (this impresses interviewers):

"This also makes it easy to unit test — each strategy is tested in isolation, 
and existing tests don't need to change when new strategies are added."

Bonus: If They Ask "What Pattern Is This?"
This is the Strategy Pattern — one of the most common design patterns. 
Mentioning that shows you understand the connection between SOLID principles and design patterns.

Quick Summary Cheat Sheet
Point	What to Say
Principle
Open for extension, closed for modification
Problem
if/elif chains force modification for every new type
Solution
Abstract base class + separate implementations
Benefit
New features = new classes, zero changes to existing code
Testing
Each strategy tested independently, existing tests untouched
Pattern name
Strategy Pattern
"""
from abc import ABC, abstractmethod


class DiscountCalculatorBad:
    def calculate_discount(self, discount_type: str, amount: float) -> float:
        if discount_type == "flat":
            return amount - 10
        elif discount_type == "percentage":
            return amount * 0.9
        else:
            raise ValueError(f"Invalid discount type: {discount_type}")
    

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, amount: float) -> float:
        pass


class FlatDiscountStrategy(DiscountStrategy):
    def __init__(self, discount_amount: float) -> None:
        self.discount_amount = discount_amount
    
    def calculate_discount(self, amount: float) -> float:
        return amount - self.discount_amount

class PercentageDiscountStrategy(DiscountStrategy):
    def __init__(self, discount_percentage: float) -> None:
        self.discount_percentage = discount_percentage
    
    def calculate_discount(self, amount: float) -> float:
        return amount * (1 - self.discount_percentage)


class DiscountCalculator:
    """
    This class is responsible for calculating the discount based on the discount strategy.
    """
    def calculate_discount(self, discount_strategy: DiscountStrategy, amount: float) -> float:
        return discount_strategy.calculate_discount(amount)


if __name__ == "__main__":
    discount_calculator = DiscountCalculator()
    flat_discount_strategy = FlatDiscountStrategy(10)
    percentage_discount_strategy = PercentageDiscountStrategy(0.1)
    print(discount_calculator.calculate_discount(flat_discount_strategy, 100))
    print(discount_calculator.calculate_discount(percentage_discount_strategy, 100))