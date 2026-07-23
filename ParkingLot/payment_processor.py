from abc import ABC, abstractmethod
from common_enum import PaymentMethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class PaymentProcessorFactory():
    def get_payment_processor(self, payment_method: PaymentMethod) -> PaymentProcessor:
        if payment_method == PaymentMethod.UPI:
            return UPIPaymentProcessor()
        elif payment_method == PaymentMethod.CREDIT_CARD:
            return CreditCardPaymentProcessor()
        elif payment_method == PaymentMethod.DEBIT_CARD:
            return DebitCardPaymentProcessor()
        else:
            raise ValueError(f"Invalid payment method: {payment_method}")

class UPIPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing payment of {amount} via UPI")
        return True

class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing payment of {amount} via Credit Card")
        return True

class DebitCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing payment of {amount} via Debit Card")
        return True
