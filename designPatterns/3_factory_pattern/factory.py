"""
Factory pattern - 
This pattern is use to encapsulate the object creation logic and used to hide concrete classes from client.
It is used when the object creation is decided at runtime
DI is used when the object creation is defined at startup
Registery Pattern avoids if/else and follows Open/Closed Principle
There are three types of factory patterns:
1. Simple Factory (Static Method) - creates one product
3. Abstract Factory (Multiple Product Families) - used when family of related product needs to be created.

"""

from abc import ABC, abstractmethod

# Abstract product
class paymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


# Concrete products
class GooglePayGateway(paymentGateway):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def process_payment(self, amount: float) -> bool:
        return True

class StripeGateway(paymentGateway):
    def process_payment(self, amount: float) -> bool:
        return True

class RazorpayGateway(paymentGateway):
    def process_payment(self, amount: float) -> bool:
        return True

# factory with registry pattern
class PaymentGatewayFactory:
    _payment_gateways = {
        "googlePay": GooglePayGateway,
        "stripe": StripeGateway,
        "razorpay": RazorpayGateway
    }

    @staticmethod
    def create(gateway_type: str, **kwargs) -> paymentGateway:
        if gateway_type not in PaymentGatewayFactory._payment_gateways:
            raise ValueError(f"Invalid gateway type: {gateway_type}")
        
        gateway_class = PaymentGatewayFactory._payment_gateways[gateway_type]
        return gateway_class(**kwargs)

    @classmethod
    def register(cls, gateway_type: str, gateway_class: type):
        cls._payment_gateways[gateway_type] = gateway_class


# client
class OrderService:
    def __init__(self, payment_gateway: paymentGateway):
        self.payment_gateway = payment_gateway

    def process_payment(self, amount: float) -> bool:
        self.payment_gateway.process_payment(amount)
        return True


if __name__ == "__main__":
    _config = {
        "googlePay": {'api_key': '1234567890'},
        "stripe": {'api_key': '1234567890'},
        "razorpay": {'api_key': '1234567890'}
    }

    google_pay_gateway = PaymentGatewayFactory.create("googlePay", **_config["googlePay"])
    stripe_gateway = PaymentGatewayFactory.create("stripe", **_config["stripe"])
    razorpay_gateway = PaymentGatewayFactory.create("razorpay", **_config["razorpay"])

    order_service = OrderService(google_pay_gateway)
    order_service.process_payment(100)